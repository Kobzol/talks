import typing
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class ButtonInactive:
    pass


@dataclass
class ButtonHover:
    timer: timedelta


@dataclass
class ButtonSelected:
    pass


ButtonState = ButtonInactive | ButtonHover | ButtonSelected

SELECT_TIME = timedelta(seconds=3)


def update_state(
    state: ButtonState,
    hover: bool,
    delta_time: timedelta
) -> ButtonState:
    match state:
        case ButtonInactive():
            if hover:
                return ButtonHover(timer=timedelta())
            return state
        case ButtonHover(timer):
            if not hover:
                return ButtonInactive()
            if timer + delta_time > SELECT_TIME:
                return ButtonSelected()
            return ButtonHover(timer=state.timer + delta_time)
        case ButtonSelected():
            if not hover:
                return ButtonInactive()
            return state
        case _ as unreachable:
            typing.assert_never(unreachable)
