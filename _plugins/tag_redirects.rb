# frozen_string_literal: true

# Redirects for tag pages that no longer exist. The blog's ~100 free-form tags
# were folded into the topics in _data/topics.yml; _data/tag_redirects.yml maps
# each retired tag to the topic that now covers it, and this turns every entry
# into a /tags/<old>/ page forwarding to /tags/<topic>/ — rendered by
# jekyll-redirect-from, so it matches the site's other redirects (meta refresh,
# canonical, kept out of the sitemap).
module SiteTagRedirects
  class Generator < Jekyll::Generator
    safe true
    # After jekyll-redirect-from's own generator: it walks site.pages and would
    # choke on the RedirectPages added here, and it installs the layout they use.
    priority :lowest

    def generate(site)
      redirects = site.data["tag_redirects"] || {}
      topics = site.data["topics"] || {}

      redirects.each do |old_tag, topic|
        unless topics.key?(topic)
          Jekyll.logger.warn "Tag redirects:", "#{old_tag} -> #{topic} is not a topic in _data/topics.yml"
          next
        end
        next if topics.key?(old_tag) # still a live topic page

        site.pages << JekyllRedirectFrom::RedirectPage.from_paths(site, "/tags/#{old_tag}/", "/tags/#{topic}/")
      end
    end
  end
end
