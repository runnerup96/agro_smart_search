import random
import json


def sample_object(entity_features_dict):
    entity = random.choice(list(entity_features_dict.keys()))
    
    # select filled attributes
    used_attr_names = []
    for attr in entity_features_dict[entity]:
        if len(entity_features_dict[entity][attr]) > 0:
            used_attr_names.append(attr)
            
    random_attrs_num = random.randint(1, len(used_attr_names))
    random_attrs = random.sample(used_attr_names, random_attrs_num)
    
    result_dict = dict()
    for attr in entity_features_dict[entity]:
        if attr in random_attrs:
            search_number = len(entity_features_dict[entity][attr]) if len(entity_features_dict[entity][attr]) < 5 else 5
            val_num = random.randint(1, search_number)
            rand_values = random.sample(entity_features_dict[entity][attr], val_num)
            result_dict[attr] = rand_values
        else:
            result_dict[attr] = []

    
    return entity, result_dict


class Finder:
    def __init__(self, plant2feature_dict, plant2display_data, top_n=5):
        self.plant2feature_dict = plant2feature_dict
        self.plant2display_data = plant2display_data
        self.top_n = top_n
        

    def search(self, attr_dict):
        
        scored_entities_list = []
        for entity in self.plant2feature_dict:
            entity_score, non_zero_attrs = 0, 0
            for key in attr_dict:
                if len(attr_dict[key]) > 0:
                    input_attr_vals = set(attr_dict[key])
                    doc_attr_vals = set(self.plant2feature_dict[entity][key])

                    intersect = doc_attr_vals.intersection(input_attr_vals)
                    intersect_score = len(intersect) / len(input_attr_vals)
                    entity_score += intersect_score
                    non_zero_attrs += 1
            entity_score = entity_score / non_zero_attrs
            scored_entities_list.append([entity, entity_score])
        
        sorted_scored_entities_list = sorted(scored_entities_list, key=lambda x: x[1], reverse=True)[:self.top_n]
        search_responce = []
        for name, score in sorted_scored_entities_list:
            entity_original_name = self.plant2display_data[name]['original_name']
            entity_definition = self.plant2display_data[name]['definition']
            entity_attributes = self.plant2feature_dict[name]
            
            result_dict = dict()
            result_dict['original_name'] = entity_original_name
            result_dict['entity_definition'] = entity_definition
            result_dict['entity_attributes'] = {key: entity_attributes[key][:5] for key in entity_attributes}
            
            result_dict['search_score'] = score
            result_dict['entity_name'] = name
            
            search_responce.append(result_dict)
        
        return search_responce
    
if __name__ == "__main__":
    display_dict = json.load(open('data/display_dict.json', 'r'))
    feature_dict = json.load(open('data/full_features_dict.json', 'r'))
    finder_instance = Finder(feature_dict, display_dict)
    entity, entity_attr = sample_object(feature_dict)
    print("Expected entity: ", entity)
    print("Input attributes: ", entity_attr)
    print('Result')
    result = finder_instance.search(entity_attr)
    print(result)