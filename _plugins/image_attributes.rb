# frozen_string_literal: true

# Width, height and lazy loading for images in posts.
#
# Markdown images come out of kramdown as a bare <img src alt>. Without
# dimensions the browser cannot reserve space, so text jumps as each image
# arrives (layout shift, a Core Web Vitals metric). After a post renders, every
# <img> pointing at a local file gets its intrinsic width and height read from
# the file header, and every image but the first gets loading="lazy" — the
# first is the likeliest largest paint and should load straight away.
module SiteImageAttributes
  module Dimensions
    module_function

    # [width, height] for PNG, GIF, JPEG and WebP files, or nil.
    def of(path)
      File.open(path, "rb") do |file|
        head = file.read(32) || ""
        if head.start_with?("\x89PNG".b)
          head[16, 8].unpack("NN")
        elsif head.start_with?("GIF8")
          head[6, 4].unpack("vv")
        elsif head.start_with?("\xFF\xD8".b)
          jpeg(file)
        elsif head[0, 4] == "RIFF" && head[8, 4] == "WEBP"
          webp(head, file)
        end
      end
    rescue SystemCallError
      nil
    end

    def jpeg(file)
      file.seek(2)
      loop do
        marker = file.read(2)
        return nil if marker.nil? || marker.getbyte(0) != 0xFF

        code = marker.getbyte(1)
        length = file.read(2).unpack1("n")
        # SOF0–SOF15 carry the frame size; C4 (DHT), C8 (JPG) and CC (DAC) do not.
        if (0xC0..0xCF).cover?(code) && ![0xC4, 0xC8, 0xCC].include?(code)
          height, width = file.read(5).unpack("xnn")
          return [width, height]
        end
        file.seek(length - 2, IO::SEEK_CUR)
      end
    end

    def webp(head, file)
      data = head + (file.read(8) || "")
      case data[12, 4]
      when "VP8 " then [data[26, 2].unpack1("v") & 0x3FFF, data[28, 2].unpack1("v") & 0x3FFF]
      when "VP8L"
        b0, b1, b2, b3 = data[21, 4].bytes
        [1 + (((b1 & 0x3F) << 8) | b0), 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))]
      when "VP8X"
        w = data[24, 3].bytes
        h = data[27, 3].bytes
        [1 + w[0] + (w[1] << 8) + (w[2] << 16), 1 + h[0] + (h[1] << 8) + (h[2] << 16)]
      end
    end
  end

  IMG = /<img\b[^>]*>/i.freeze

  def self.apply(doc)
    return unless doc.output&.include?("<img")

    site = doc.site
    index = -1
    doc.output = doc.output.gsub(IMG) do |tag|
      index += 1
      src = tag[/\ssrc="([^"]+)"/i, 1]
      if src&.start_with?("/") && !tag.match?(/\swidth=/i)
        size = Dimensions.of(File.join(site.source, src.split(/[?#]/).first))
        tag = tag.sub(/<img\b/i, %(<img width="#{size[0]}" height="#{size[1]}")) if size
      end
      tag = tag.sub(/<img\b/i, '<img loading="lazy"') if index.positive? && !tag.match?(/\sloading=/i)
      tag.match?(/\sdecoding=/i) ? tag : tag.sub(/<img\b/i, '<img decoding="async"')
    end
  end
end

Jekyll::Hooks.register :posts, :post_render do |post|
  SiteImageAttributes.apply(post)
end
