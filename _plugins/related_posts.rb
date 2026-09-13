# frozen_string_literal: true

# Related posts by topic. Every post gets `page.related`: up to three other
# posts ranked by how many topics (tags) they share, the nearest in time
# breaking ties. Posts sharing nothing are never offered.
#
# Jekyll's own `site.related_posts` is either LSI (slow, needs a gem) or simply
# the newest posts, neither of which says anything about the post at hand.
module SiteRelatedPosts
  class Generator < Jekyll::Generator
    safe true
    priority :low

    LIMIT = 3

    def generate(site)
      posts = site.posts.docs
      posts.each do |post|
        tags = Array(post.data["tags"])
        next post.data["related"] = [] if tags.empty?

        scored = posts.filter_map do |other|
          next if other.equal?(post)

          shared = (tags & Array(other.data["tags"])).size
          [other, shared, (other.date - post.date).abs] if shared.positive?
        end
        post.data["related"] = scored
          .sort_by { |_, shared, distance| [-shared, distance] }
          .first(LIMIT)
          .map(&:first)
      end
    end
  end
end
