"""Backend implementations (rough-in) for interactive prompt devices:

- serial_prompt_talker: drive a 'Diags$ ' style shell over serial (RS-232/USB)
- ssh_prompt_talker: drive the same style shell over SSH

Both expose a minimal API:
  class Talker:
      def send(self, command: str) -> tuple[str, str]  # returns (status, body)
      def close(self) -> None
"""