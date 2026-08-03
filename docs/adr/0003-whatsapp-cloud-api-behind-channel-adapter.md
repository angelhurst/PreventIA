# 0003 — WhatsApp Cloud API test number behind a channel adapter

**Status:** Accepted
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

The product's premise is that an older adult answers a daily check-in on WhatsApp, on their own
phone, in their own words. The Lab's demo is a recorded video shown to a panel that includes
clinical and management judges, and winning prototypes enter an adoption-evaluation pathway inside a
real health network.

WhatsApp Business API access normally implies Meta business verification, which takes longer than
the two days available. The prototype therefore needs a channel that is real, works this week, and
could survive contact with an actual patient.

## Decision

Use **Meta's WhatsApp Cloud API test number** as the patient channel, and keep the agent core
**channel-agnostic** behind an adapter interface in `channels/`.

The test number is free, requires no business verification, is provisioned in under 30 minutes, and
sends real WhatsApp messages to real phones. It talks only to up to five OTP-verified recipient
numbers, which is a production limitation and precisely the isolation a demo wants.

Two operational constraints are consequences of this choice and are recorded in the runbook:

- The console access token expires in 60 minutes. A System User permanent token must exist before
  demo day.
- Free-form messages only flow inside a 24-hour window opened by an inbound message from the
  recipient. The recording therefore opens with the patient sending a message, which matches the
  product story of a patient answering a check-in.

Nothing below `channels/` imports a WhatsApp client. `channels/local_console.py` implements the same
interface with no telephony at all.

Backup ladder, in order: Cloud API test number, Twilio Sandbox, local console.

## Consequences

- The demo shows a real WhatsApp conversation on a real phone, with no staging and nothing faked.
- The adapter seam makes "this could run on SMS, voice, or a clinic portal" a true statement rather
  than an aspiration, and it means a hostile venue network downgrades the demo instead of ending it.
- Five recipients is enough for the team and no one else. Any wider pilot requires business
  verification, which is a Phase 5 problem.
- Inbound messages need a public HTTPS endpoint, so a tunnel is a dependency of the live demo. The
  local console path exists because that dependency can fail.
- Meta ends the free 24-hour service window on 1 October 2026, after which in-window replies bill per
  message. Irrelevant to the Lab, relevant to any pilot cost estimate.

## Alternatives considered

**Twilio Sandbox.** Five minutes to set up, no Meta app at all, recipients join with a code.
Retained as the backup rather than the primary: it sends from a shared US number, which weakens the
credibility of the demo, and sandbox sessions expire after three days.

**A personal WhatsApp account driven through a reverse-engineered client** (whatsmeow, Baileys, or
an MCP server wrapping either). Best-looking demo and the least setup. Rejected outright: it
violates Meta's terms regardless of message content, carries a real and unpredictable ban risk on a
personal number, and demonstrates a channel that could never legally carry a patient. In a lab
judged on a pathway to adoption inside a health network, that is a hole a management-criteria judge
will find.

**Local chat harness only, no telephony.** Spends both days on clinical logic. Rejected because the
daily-check-in-on-your-own-phone premise is most of what makes the product legible in 3 minutes.

**Staging or faking the messages.** Rejected. The Cloud API test number removes any reason to, and
the panel is evaluating toward a real pilot.
