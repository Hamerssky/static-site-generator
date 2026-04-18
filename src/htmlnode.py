class HTMLNode:
    """HTML node class, represents inline or bloc level snippets like html tags and text"""
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        res = ""
        for key, val in self.props.items():
            res += f" {key}=\"{val}\""
        return res
    
    def __repr__(self):
        return f"Tag: {self.tag}\n\
            Value: {self.value}\n\
            Children: {self.children}\n\
            Props: {self.props}\n"