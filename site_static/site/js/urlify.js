function URLify(s, num_chars) {
    // changes, e.g., "Petty theft" to "petty_theft"
    // remove all these words from the string before urlifying
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for", "from",
                  "is", "in", "into", "like", "of", "off", "on", "onto", "per",
                  "since", "than", "the", "this", "that", "to", "up", "via",
                  "with"];
    r = new RegExp('\\b(' + removelist.join('|') + ')\\b', 'gi');
    s = s.replace(r, '');
    /* ADDED 2006-11-01 */
    s = s.replace(/[Ää]/gi, 'ae');    // change german letters
    s = s.replace(/[Öö]/gi, 'oe');    // change german letters
    s = s.replace(/[Üü]/gi, 'ue');    // change german letters
    s = s.replace(/[ß]/gi, 'ss');    // change german letters
    /* /ADDED */
    s = s.replace(/[^_\-A-Z0-9\s]/gi, '');  // remove unneeded chars
    s = s.replace(/^\s+|\s+$/g, ''); // trim leading/trailing spaces
    s = s.replace(/[-\s]+/g, '-');   // convert spaces to hyphens
    s = s.toLowerCase();             // convert to lowercase
    return s.substring(0, num_chars);// trim to first num_chars chars
}
