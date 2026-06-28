from __future__ import annotations

from ..config import RobotConfig
from ..state import SessionState, Tier
from ..voice.orchestrator import VoiceOrchestrator
from ..content import load_flows


class GuidedFlowSkill:
  def run(
      self,
      voice: VoiceOrchestrator,
      config: RobotConfig,
      state: SessionState,
      flow_id: str,
  ) -> None:
      data = load_flows()
      flow = next((f for f in data["flows"] if f["id"] == flow_id), None)
      if not flow:
          voice.say(f"I don't have a flow called {flow_id}.", force=True)
          return

      state.in_flow = flow_id
      voice.say(
          f"Running {flow['title']}. {flow.get('trigger', '')}. "
          "Say 'stop' any time to exit.",
          force=True,
      )

      for i, step in enumerate(flow["steps"]):
          state.flow_step = i
          if flow_id == "doom-loop" and i == 0:
              voice.say(step, force=True)
          else:
              voice.say(step, force=True)

          if config.tier in ("red", "black") and i < len(flow["steps"]) - 1:
              cont = voice.ask("Ready for next step? Say yes or stop.")
              if cont.lower() in ("stop", "quit", "no"):
                  break
          else:
              voice.listen()  # pause for user — press enter in console mode

      if flow.get("success"):
          voice.say("Success looks like: " + ". ".join(flow["success"]), force=True)

      if flow.get("fallback"):
          voice.say(f"If that didn't help: escalate to {flow['fallback']}.", force=True)

      state.in_flow = None
      state.flow_step = 0
