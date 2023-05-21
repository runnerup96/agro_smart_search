import random
from typing import Dict, List, Tuple


def sample_object(entity_features_dict: Dict) -> Tuple[str, Dict]:
    """
    Function to sample an entity from the given dictionary and return a subset of its attributes.

    Args:
        entity_features_dict (Dict): A dictionary containing entity names as keys and another dictionary of their attributes as values.

    Returns:
        Tuple[str, Dict]: A tuple containing a randomly selected entity name and a dictionary of selected attributes.
    """
    entity = random.choice(list(entity_features_dict.keys()))

    # select filled attributes
    used_attr_names = [
        attr
        for attr in entity_features_dict[entity]
        if entity_features_dict[entity][attr]
    ]

    random_attrs_num = random.randint(1, len(used_attr_names))
    random_attrs = random.sample(used_attr_names, random_attrs_num)

    result_dict = {
        attr: (
            random.sample(
                entity_features_dict[entity][attr],
                val_num := random.randint(
                    1, min(5, len(entity_features_dict[entity][attr]))
                ),
            )
            if attr in random_attrs
            else []
        )
        for attr in entity_features_dict[entity]
    }
    return entity, result_dict


class Finder:
    """
    Class to encapsulate the finding algorithm.
    """

    def __init__(
        self,
        plant2feature_dict: Dict,
        plant2display_data: Dict,
        popularity_dict: Dict,
        top_n: int = 5,
    ):
        """
        Initializer for Finder.

        Args:
            plant2feature_dict (Dict): A dictionary mapping plant names to their features.
            plant2display_data (Dict): A dictionary mapping plant names to their display data.
            popularity_dict (Dict): A dictionary mapping plant names to their popularity scores.
            top_n (int): The number of top results to return. Default is 5.
        """
        self.plant2feature_dict = plant2feature_dict
        self.plant2display_data = plant2display_data
        self.popularity_dict = popularity_dict
        self.top_n = top_n

    def search(self, attr_dict: Dict) -> List[Dict]:
        """
        Method to perform the search operation based on attribute dictionary.

        Args:
            attr_dict (Dict): A dictionary containing attributes to be searched for.

        Returns:
            List[Dict]: A list of dictionaries each representing a plant entity that matches the search.
        """
        scored_entities_list = [
            [
                entity,
                sum(
                    len(
                        set(self.plant2feature_dict[entity][key]).intersection(
                            set(attr_dict[key])
                        )
                    )
                    / len(set(attr_dict[key]))
                    for key in attr_dict
                    if attr_dict[key]
                )
                / sum(bool(attr_dict[key]) for key in attr_dict)
                + self.popularity_dict[entity] / 5,
            ]
            for entity in self.plant2feature_dict
        ]

        sorted_scored_entities_list = sorted(
            scored_entities_list, key=lambda x: x[1], reverse=True
        )[: self.top_n]

        return [
            {
                "original_name": self.plant2display_data[name]["original_name"],
                "entity_definition": self.plant2display_data[name]["definition"],
                "entity_attributes": self.plant2feature_dict[name],
                "search_score": score,
                "entity_name": name,
                "popularity": self.popularity_dict[name],
            }
            for name, score in sorted_scored_entities_list
        ]
