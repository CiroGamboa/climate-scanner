#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:36:48 2022

@author: cirogam
"""

from neomodel import (config, StructuredNode, StringProperty,
                      Relationship, ZeroOrMore,
                      StructuredRel, AliasProperty, UniqueIdProperty)  # work with neo4j

config.DATABASE_URL = "bolt://neo4j:test@localhost:7687"

# TODO: Run query for setting unique name
# TODO: Set logic for existing nodes

class BasicRel(StructuredRel):
	rel = StringProperty(required=True)
	name = AliasProperty(to='rel')

class Node(StructuredNode):
	uid = UniqueIdProperty()
	name = StringProperty(required=True, unique_index=True)
	entity = StringProperty(required=True, unique_index=False)
	entity_type = name = StringProperty(required=True, unique_index=False)
	wiki_classes = name = StringProperty(required=True, unique_index=False)
	url = name = StringProperty(required=True, unique_index=True)
	dbpedia_uri = name = StringProperty(required=True, unique_index=True)
	related_to = Relationship('Node', 'RELATED_TO', cardinality=ZeroOrMore, model=BasicRel)

	@property
	def serialize(self):
		return {
					'uid' : self.uid,
					'name': self.name,
					'entity': self.entity,
					'entity_type': self.entity_type,
					'wiki_classes': self.wiki_classes,
					'url': self.url,
					'dbpedia_uri': self.dbpedia_uri,
			}



class GraphConstructor:

	def __init__(self):
		self.nodes = []
		#self.create_nodes(entities)

	def define_rels(self):
		pass

	def get_nodes(self,entity_type=None):
		#TODO: Avoid returning the arrays as strings

		nodes = None
		try:
			if(entity_type != None):
				# Return set of nodes
				result_nodes = Node.nodes.filter(entity=entity_type)
			else:
				result_nodes = Node.nodes.all()

			nodes = [n.serialize for n in result_nodes]

		except Exception as e:
			print(str(e))

		print(nodes)
		return nodes


	def create_nodes(self, entities):

		success = False
		try:
			for ann in entities:
				new_node = Node(
					name = ann[0] if ann[0]!= None else "",
					entity = ann[1] if ann[1]!= None else "",
					entity_type = ann[2]['entityType'] if ann[2]['entityType']!= None else [],
					wiki_classes = ann[2]['wiki_classes'] if ann[2]['wiki_classes']!= None else [],
					url = ann[2]['url'] if ann[2]['url']!= None else "",
					dbpedia_uri = ann[2]['dbPediaIri'] if ann[2]['dbPediaIri']!= None else ""
					   ).save()

				for node in self.nodes:
					new_node.related_to.connect(node,{'rel':'related'})

				self.nodes.append(new_node)

			success = True

		except Exception as e:
			print(str(e))

		return success




