import pydantic


class BaseModel(pydantic.BaseModel):
    pass


class MdadmStates:
    Active = "active"
    Checking = "checking"


class MdadmActions:
    Check = "check"
    Repair = "repair"


class MdadmOutput(BaseModel):
    device: str
    state_list: list[str] = []
    check_status: str | None = None

    def is_active(self):
        return MdadmStates.Active in self.state_list

    def is_checking(self):
        return MdadmStates.Checking in self.state_list

    @property
    def check_status_percentage(self) -> int | None:
        return parse_percentage(self.check_status)


def parse_percentage(s: str) -> int | None:
    if not s:
        return None

    percentage_str = s.split("%")[0]
    if percentage_str.isnumeric():
        return int(percentage_str)
