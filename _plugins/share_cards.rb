# frozen_string_literal: true

# Share images for link previews (Slack, Teams, email, LinkedIn).
#
# jekyll-seo-tag only writes og:image when a page has its own `image:`, so
# without this most pages sent no picture and previews showed an empty box.
# Before rendering, this gives every HTML page an `image:`:
#
#   - a page that sets `image:` keeps it (e.g. cali.html);
#   - a page with an `icon:` gets its own card, /assets/img/og/<page>.png:
#     that icon in a ring over the faded BIRD logo, with no words;
#   - every other page (the home page, a page with no `icon:`, or
#     `share_card: false`) gets the site-wide logo card from `image:` in
#     _config.yml.
#
# scripts/share_cards.py draws the cards after the build, from the list this
# file saves in .jekyll-cache/share-cards.json.
#
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".

require "json"
require "fileutils"

module BirdLabShareCards
  CARD_DIR = "/assets/img/og"
  SKIP_URLS = ["/404.html"].freeze

  # "/lab-guide/data-management/" -> "lab-guide-data-management"
  def self.slug(url)
    url.sub(%r{\.html\z}, "").gsub(%r{[^A-Za-z0-9]+}, "-").gsub(%r{\A-|-\z}, "").downcase
  end
end

Jekyll::Hooks.register :site, :pre_render do |site|
  default_image = site.config["image"]
  cards = []

  docs = site.collections.values.select(&:write?).flat_map(&:docs)
  (site.pages + docs).each do |item|
    next unless item.output_ext == ".html"
    next if item.data.key?("image")                 # chosen by hand: keep it
    next if BirdLabShareCards::SKIP_URLS.include?(item.url)

    icon = item.data["icon"].to_s.strip
    if item.url == "/" || icon.empty? || item.data["share_card"] == false
      item.data["image"] = default_image if default_image
      next
    end

    title = item.data["title"].to_s.strip
    path = "#{BirdLabShareCards::CARD_DIR}/#{BirdLabShareCards.slug(item.url)}.png"
    item.data["image"] = {
      "path" => path,
      "width" => 1200,
      "height" => 630,
      "alt" => "#{title}: the page's icon over the BIRD Lab logo",
    }
    cards << { "path" => path, "icon" => icon, "title" => title }
  end

  manifest = {
    "site_url" => "#{site.config['url']}#{site.config['baseurl']}",
    "cards" => cards.uniq { |c| c["path"] },
  }
  json = JSON.pretty_generate(manifest)
  out = site.in_source_dir(site.config["cache_dir"] || ".jekyll-cache", "share-cards.json")
  FileUtils.mkdir_p(File.dirname(out))
  File.write(out, json) unless File.exist?(out) && File.read(out, encoding: "UTF-8") == json
end
