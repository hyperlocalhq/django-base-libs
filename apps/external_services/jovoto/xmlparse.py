from xml.dom.minidom import parseString
from xml.dom.minidom import Node

"""
functions used for xml parsing for external applications
"""

def get_value(nodelist):
    """ little helper function for DOM parsing """
    try:
        node = nodelist[0]
        if node.firstChild.nodeType == Node.TEXT_NODE: 
            return node.firstChild.data.strip()
    except: 
        pass
    return "" 

def parse_idea_list(xml):
    """
    use the python minidom parser to extract the required information.
    (maybe this one is too slow)
    """
    idea_list = []
    doc = parseString(xml)
    ideas = doc.getElementsByTagName('idea')
    for idea in ideas:
        media0 = idea.getElementsByTagName("media")[0]
        author = idea.getElementsByTagName("author")[0]
        idea_list.append({
            'name' : get_value(idea.getElementsByTagName("name")),
            'description' : get_value(idea.getElementsByTagName("description")),
            'pubdate' : get_value(idea.getElementsByTagName("pubDate")),
            'link' : get_value(idea.getElementsByTagName("link")),
            'guid' : get_value(idea.getElementsByTagName("guid")),
            'rating' : get_value(idea.getElementsByTagName("rating")),
            
            'author_username' : get_value(author.getElementsByTagName("username")),
            'author_city' : get_value(author.getElementsByTagName("city")),
            'author_country' : get_value(author.getElementsByTagName("country")),
            'author_icon' : get_value(author.getElementsByTagName("icon")),
            
            'media0_type' : get_value(media0.getElementsByTagName("type")),
            'media0_thumb' : get_value(media0.getElementsByTagName("thumb")),
            'media0_medium' : get_value(media0.getElementsByTagName("medium")),
            'media0_big' : get_value(media0.getElementsByTagName("big")),
            'media0_path' : get_value(media0.getElementsByTagName("path")),
        })
    return idea_list

def parse_idea_details(xml):
    """
    parses idea details from xml
    """
    doc = parseString(xml)
    idea = doc.getElementsByTagName('idea')[0]
    idea_dict = {}
    idea_dict['name'] = get_value(idea.getElementsByTagName("name"))
    idea_dict['description'] = get_value(idea.getElementsByTagName("description"))
    idea_dict['updated_at'] = get_value(idea.getElementsByTagName("updated_at"))
    idea_dict['pubdate'] = get_value(idea.getElementsByTagName("pubDate"))
    idea_dict['link'] = get_value(idea.getElementsByTagName("link"))
    idea_dict['rating'] = get_value(idea.getElementsByTagName("rating"))

    author = idea.getElementsByTagName("author")[0]
    idea_dict['author_username'] = get_value(author.getElementsByTagName("username"))
    idea_dict['author_city'] = get_value(author.getElementsByTagName("city"))
    idea_dict['author_country'] = get_value(author.getElementsByTagName("country"))
    idea_dict['author_icon'] = get_value(author.getElementsByTagName("icon"))
    
    media_list = []
    medias = idea.getElementsByTagName("media")
    for media in medias:
        media_list.append({
            'media_type' : get_value(media.getElementsByTagName("type")),
            'media_thumb' : get_value(media.getElementsByTagName("thumb")),
            'media_medium' : get_value(media.getElementsByTagName("medium")),
            'media_big' : get_value(media.getElementsByTagName("big")),
            'media_path' : get_value(media.getElementsByTagName("path")),
        })
    idea_dict['media'] = media_list            
    return idea_dict
