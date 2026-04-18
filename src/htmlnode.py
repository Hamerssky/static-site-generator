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
        if not self.props:
            return ""
        res = ""
        for key, val in self.props.items():
            res += f" {key}=\"{val}\""
        return res
    
    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}\n"
    
class LeafNode(HTMLNode):
    """Leaf node class, represents last nodes in an html tree structure"""
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"Tag: {self.tag}\n\
            Value: {self.value}\n\
            Props: {self.props}\n"
        
class ParentNode(HTMLNode):
    """Parent node class, represents nodes with children"""
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        
        res = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            res += child.to_html()

        res += f"</{self.tag}>"

        return res
