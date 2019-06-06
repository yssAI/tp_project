from server3.entity.tag import Tag


class GeneralService:
    @classmethod
    def update_tags(cls, oldtags, newtags, entity_type, entities):
        tags_need_insert = [tag for tag in newtags if tag not in oldtags]
        tags_need_pull = [tag for tag in oldtags if tag not in newtags]

        # update tags
        [Tag.add_or_insert(id_=tag, entity_type=entity_type,
                           entities=entities) for tag in tags_need_insert]
        [Tag.pull(id_=tag, entity_type=entity_type,
                  entities=entities) for tag in tags_need_pull]

