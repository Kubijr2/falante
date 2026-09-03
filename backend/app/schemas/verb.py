from pydantic import BaseModel, ConfigDict, Field


class VerbListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    infinitive: str
    translation: str
    is_irregular: bool


class VerbDetail(VerbListItem):
    conjugations: dict[str, list[str]]


class VerbFormLookupRequest(BaseModel):
    forms: list[str] = Field(min_length=1, max_length=500)


class VerbFormLookupResult(BaseModel):
    infinitive: str
    translation: str


class VerbFormLookupResponse(BaseModel):
    # Keyed by the exact form string the client sent (not lowercased) so the
    # frontend can look up a match with a plain dict access against the
    # token it actually rendered, no re-normalization needed on that side.
    matches: dict[str, VerbFormLookupResult]
