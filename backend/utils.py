import json

def make_changes(lead):
    if lead.changes == None:
        return
    
    changes = json.loads(lead.changes)
    
    name = changes.get("name")
    website = changes.get("website")

    if name is not None:
        lead.name = name

    if website is not None:
        lead.website = website

    lead.changes = None