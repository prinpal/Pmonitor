import sys
from typing import LiteralString

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, ValidationError
from pydantic_settings import CliApp, CliPositionalArg

from .monitor import ProcessMonitor


class Cli(BaseModel):
    """A process system resource usage monitor."""

    pid: CliPositionalArg[PositiveInt] = Field(description="Process PID.")
    interval: CliPositionalArg[PositiveFloat] = Field(
        1.0, description="Monitoring interval in seconds."
    )

    def cli_cmd(self):
        pm = ProcessMonitor(self.pid, interval=self.interval)
        pm.start()

    @staticmethod
    def custom_messages(val_err: ValidationError) -> LiteralString:
        msgs = []
        for err in val_err.errors():
            msgs.append(
                f"- {err['loc'][0].upper()}: {err['msg']}, but got '{err['input']}'"  # type: ignore
            )
        return "\n".join(msgs)


def main():
    try:
        CliApp.run(Cli)
    except ValidationError as e:
        print(f"Argument parsing error:\n{Cli.custom_messages(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred when starting monitoring:\n{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
