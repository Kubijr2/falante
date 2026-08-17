from pydantic import BaseModel, ConfigDict


class VerbListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    infinitive: str
    translation: str
    is_irregular: bool


class VerbDetail(VerbListItem):
    # tense key (e.g. "present") -> [eu, ele/ela/você, nós, eles/elas/vocês]
    conjugations: dict[str, list[str]]
