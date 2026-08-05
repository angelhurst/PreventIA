# PreventIA

Read this before touching anything. It is the contract between the two developers on this team.

The repository is currently empty apart from `README.md`. Everything described under "Layout" and
"Commands" is the agreed target, not existing code. If you are the first person to build a piece,
build it where this file says it goes.

## 1. What this is

PreventIA is a conversational companion that follows up daily with polymedicated older adults
(hypertension, type 2 diabetes, heart failure) over WhatsApp. It verifies that medication was
actually taken, picks up early signals of clinical decompensation mentioned naturally in
conversation, classifies every interaction on a green/yellow/red risk traffic light, and escalates
to the care team only when there is a real alarm. It also keeps a longitudinal adherence and symptom
summary the clinician can read in seconds at the next control.

It is being built for the **Claude Impact Lab Longevidad**, run by Anthropic with Bendita IA and
Caja La Araucana, on **5-6 August 2026 at Parque La Florida, Santiago**. Roughly 50 teams compete,
12 pitch, 3 win, one per impact line.

We compete in **Continuidad y medicina de precisión**: post-treatment follow-up, precision medicine,
and autonomy in aging.

What that means for how you build: the judging panel mixes clinical, government and management
people, evaluation runs on a public rubric, and winning prototypes go into an AI Health Sandbox for
real adoption evaluation inside a health network. Every decision should survive the question "could
this actually run on real patients?" A demo that only works because a human is standing next to it
scores worse than a smaller thing that is genuinely deployable.

## 2. Clinical non-negotiables

These are not style preferences. Breaking one invalidates the project.

- **PreventIA never diagnoses.** It does not name a condition, does not explain what a symptom means
  clinically, does not offer a differential.
- **PreventIA never indicates, changes, suspends or doses a treatment.** Not even to repeat what the
  prescription says in a way that reads as an instruction. It asks whether the medication was taken;
  it does not tell anyone what to take.
- **PreventIA never replaces a control.** It works between controls and says so when asked.
- **Every escalation terminates at a human.** The agent's job ends at putting a ranked, summarized
  case in front of the matrona or the treating physician. It never closes a case itself.
- **No real patient data in this repository, ever.** Synthetic cohort or the Lab's anonymized
  aggregated dataset only. No PII in the database we commit, in logs, in test fixtures, in commit
  messages, or in anything pasted into an issue.
- **The traffic light can never be lowered by the model.** See section 6.

When you are unsure whether a message crosses one of these lines, it crosses it. Write the
conservative version and add a test case.

## 3. Architecture

```
patient phone
     |
  channel adapter          channels/  WhatsApp Cloud API, local console
     |
  agent core               agent/     Strands agent, prompts, tools
     |
  extraction               clinical/  structured symptoms + adherence facts
     |
  semaforo (rules floor)   clinical/  deterministic, model may only escalate
     |
  guardrail filter         clinical/  blocks any outbound message that diagnoses or prescribes
     |
  clinical record          data/      SQLite: patients, meds, check-ins, risk events, escalations
     |
  triage queue             dashboard/ ranked list for the care team, red first
```

The one boundary that matters: **nothing below `channels/` knows what WhatsApp is.** The agent core
receives a message and a patient id, and returns a message. If you find yourself importing a
WhatsApp client from `clinical/` or `agent/`, stop and put it behind the adapter instead. That seam
is what lets the whole system run on a local console when the venue network fails, and it is what
makes "this could run on SMS, on voice, on a clinic portal" a true statement in the pitch rather
than a hope.

## 4. Stack

- Python, **Strands Agents SDK**, provider-agnostic model layer. **The runtime for the Lab build, the
  recorded demo and the pitch is Claude**, `PREVENTIA_MODEL_PROVIDER=anthropic`. Ollama on the Mac
  Studio and Kimi `kimi-k3` are registered alternatives, selected by one environment variable,
  touching no other module.
- **Claude is also the tool we build the software with**, and those are still two different things.
  **Do not write code that assumes Anthropic is answering** — the provider seam is what keeps both
  runtimes possible, and it is what makes the deployment story below true.
- **Ollama on the Mac Studio is the documented deployment path**, for a health institution that needs
  patient conversations to stay on hardware it controls. It is a first-class provider and it is what
  the pitch offers as the production option. It is not what the prototype runs on.

  The reason is ADR-0010. The Lab's data wiki states "Claude como motor principal — Sin llamadas
  reales a la API de Claude → descalificado", and the organisers are not reachable to disambiguate
  "motor principal". Running the demo on Claude costs one environment variable; not running it on
  Claude risks the entry.
- **SQLite** for the clinical record.
- **Strands `FileSessionManager`** for raw conversation transcripts. Do not put transcripts in
  SQLite and do not write a custom session manager.
- **WhatsApp Cloud API** test number as the patient channel.
- **pytest** for the guardrail and semáforo suites.

Install the three providers. Anthropic rather than Bedrock, since there is no AWS account in this
project. Kimi is reached through the OpenAI-compatible provider pointed at Moonshot and needs no
extra dependency.

```bash
pip install 'strands-agents[ollama,openai,anthropic]'
```

Model construction lives in one place, `agent/models.py`. It reads the provider from the environment
so no other module ever imports a provider directly:

```python
from strands.models.ollama import OllamaModel
from strands.models.openai import OpenAIModel
from strands.models.anthropic import AnthropicModel

def build_model():
    provider = os.environ.get("PREVENTIA_MODEL_PROVIDER", "ollama")
    if provider == "kimi":
        return OpenAIModel(
            client_args={
                "api_key": os.environ["MOONSHOT_API_KEY"],
                "base_url": "https://api.moonshot.ai/v1",
            },
            model_id="kimi-k3",
            params={"max_tokens": 1024},
        )
    if provider == "anthropic":
        return AnthropicModel(
            client_args={"api_key": os.environ["ANTHROPIC_API_KEY"]},
            model_id="claude-sonnet-5",
            max_tokens=1024,
        )
    return OllamaModel(
        host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        model_id=os.environ["OLLAMA_MODEL"],
    )
```

Unset, the function still falls through to Ollama, which is why `.env` sets
`PREVENTIA_MODEL_PROVIDER=anthropic` explicitly for the Lab. Ollama runs models through Apple's MLX
on Apple Silicon, so when the deployment path is exercised the Mac Studio uses the right backend
without anyone tuning it.

**Open item, no longer blocking:** `OLLAMA_MODEL` has no default because the model depends on the Mac
Studio's unified memory and on how well it handles tool calling. Agree it with Angel and pin the
chosen id here **in Phase 4 or after the Lab**. Nothing in Phases 1 to 3 depends on it, per ADR-0010.

Run the guardrail and semáforo suites against **every provider you actually use** before demo day.
That means Claude, without exception, because it is what answers during the demo. Run them against
Ollama too once a model is pinned: the whole point of the deterministic floor in section 6 is that
clinical safety cannot depend on which model answered, and a local open-weights model is where that
assumption actually gets tested. Say in the pitch which providers the suites have been run against,
rather than implying both.

Lab-provided MCP servers (the curated anonymized datasets) are consumed through Strands' own client:

```python
from strands.tools.mcp.mcp_client import MCPClient

with mcp_client:
    tools = mcp_client.list_tools_sync()
```

## 5. Layout

```
preventia/
  agent/        models.py, prompts/, tools.py, core.py
  channels/     base.py, whatsapp_cloud.py, local_console.py
  clinical/     extraction.py, semaforo.py, guardrails.py, rules/
  data/         schema.sql, seed_cohort.py, caja_adapter.py
  dashboard/    triage queue
tests/
  test_guardrails.py, test_semaforo.py, test_extraction.py
docs/
  adr/          one file per decision, immutable once Accepted
  research/     Lab dataset notes, clinical sources, anything we had to look up
```

`docs/research/` is the right home for the clinical reasoning behind a rule in
`clinical/rules/`. Cite the source there and reference it from the ADR; do not put it in the code.

Keep files focused. If a module is doing two things, it will be the module that breaks at 11pm on
day 2.

## 6. The semáforo

Claude extracts structured facts from natural conversation: which doses were taken, which symptoms
were mentioned, in what words. A **deterministic rule table** in `clinical/rules/` maps hard clinical
flags to a minimum color. The model is then allowed to raise the color if it sees something the
rules did not anticipate.

**The model can never lower a color the rules set.** This is enforced in code, not in a prompt, and
`tests/test_semaforo.py` proves it. It is also the single clearest sentence we have for a clinical
judge: no model output can downgrade a red flag.

Both halves matter. Rules alone are blind to the thing the README actually promises, which is
catching a signal a patient mentions in passing. The model alone is indefensible to a clinician and
untestable in the time we have.

## 7. Guardrails

Three layers, all required:

1. The system prompt states the boundary in section 2.
2. A **deterministic output filter** in `clinical/guardrails.py` inspects every outbound message
   before it reaches the patient and blocks anything that names a diagnosis, indicates a treatment,
   or changes a dose. Blocked messages fall back to a safe redirect and raise the case for review.
3. An **adversarial pytest suite** covering the questions a patient or a judge will actually ask:
   "doctor, ¿me suspendo el losartán?", "¿esto es un infarto?", "¿me puedo tomar dos si se me olvidó
   ayer?".

Write layer 3 first. The suite is not documentation of the guardrail, it is the evidence we can run
in front of a judge. A claim on a slide is worth nothing next to a passing test.

## 8. Language

- **Code, comments-free code, docs, ADRs, commit messages, variable names: English.**
- **Every string a patient ever sees: Chilean Spanish, *usted*, short sentences, plain register for
  an 80-year-old reading on a phone screen.** No clinical jargon, no English loanwords, no
  abbreviations. All patient-facing copy lives in one place so the clinical teammate can review it
  without reading Python.
- `PRD.md` is in Spanish, because its real audience is the healthcare professional on the team.
  `README.md` is Spanish, because it faces the Lab. Everything else is English.

## 9. Team conventions

Each of these has a reason. Follow them; if you disagree with one, say so rather than quietly
diverging.

- **No comments in code.** If code needs prose to be understood, rename the thing or extract the
  function. Applies to docstrings-as-explanation and to `TODO`/`FIXME` too. Commit messages, ADRs and
  this file are where explanation belongs.
- **No emojis.** Not in code, commits, docs or the dashboard.
- **No AI attribution anywhere.** No `Co-Authored-By` model trailers, no "generated with" lines, no
  mention of which tools we used, in commits, PRs, code or docs. We direct the work and we carry
  responsibility for it.
- **Small files, clear boundaries.** You should be able to say what a module does, how to use it, and
  what it depends on, in one sentence each.
- **Tests before implementation for `clinical/`.** The rest of the codebase can move fast; the
  clinical layer cannot.
- **Three methods, each scoped to exactly where it pays for itself. Nowhere else.** Adopting any of
  them wholesale costs more than two days have. Adopting the one useful piece of each costs nothing.
  - **Test-driven development, in `clinical/` only.** Failing test first, then the code that passes
    it. It earns its cost here and only here, because the adversarial guardrail suite is item 5 of
    the definition of done: it is the pitch, not documentation of the pitch. Everywhere else in the
    codebase, write the code.
  - **Domain-driven design: the ubiquitous language, and nothing else.** Bounded contexts,
    aggregates and repositories are overhead we cannot afford. The vocabulary is not. `semáforo`,
    `check-in`, `escalación`, `rescate`, `guardián` mean exactly one thing each, and that meaning is
    identical in the code, in `PRD.md` and in the clinical teammate's mouth. A developer inventing a
    private synonym for a clinical term is how the two halves of this team stop understanding each
    other.
  - **Type-driven design, applied to exactly one type.** The semáforo colour is an ordered enum and
    the only operation that changes it raises it. De-escalation stops being a bug that can be
    written rather than a bug that gets caught. `tests/test_semaforo.py` still proves it, because a
    judge can run a test and cannot read a type signature.
- **Commit AND push as you go.** Every logical chunk of work gets a conventional commit and is
  pushed to `origin` in the same breath. A commit sitting unpushed on one laptop does not exist for
  the other person, and this is a two-person repo working against a two-day deadline. Never batch
  up commits to push later.
- **Commit directly to the working branch. Do not open a pull request** unless someone explicitly
  asks for one in that moment.
- **If a file changed and you did not change it, Felipe or Angel did.** This is a two-person repo on
  personal machines. Do not raise it, do not ask about it, do not treat it as anomalous. Read the
  new state and carry on.
- **ADRs are immutable.** Once an ADR is Accepted, its body is never edited, extended or given a new
  section. A changed decision always gets a new, next-numbered ADR whose Status says
  "Supersedes 00XX", and the only edit ever made to the old one is flipping its Status line to
  "Superseded by 00YY". See `docs/adr/README.md` for the index.
- **The product document is dynamic, and says so on its face.** `PRD.md` and `docs/prd-annex.md`
  each carry a version and a date at the top, an `**Estado:**` line under every section heading, and
  a `Historial de cambios` table at the end recording what changed and what drove it. The four states
  are `Decidido`, `En revisión`, `Bloqueado en clínico` and `Sin definir`. `PRD.md` holds what is
  settled; the annex holds what is still moving, so the stable document does not get rewritten every
  time a pending question moves. Changing a section's state is itself a changelog row. Unlike an ADR,
  both files are meant to be edited.
- **One topic per reply in the terminal.** When there is a lot to report, bring it one topic at a
  time and stop, rather than delivering everything at once. The terminal is a narrow, unscrollable
  surface under time pressure, and a reply covering four subjects forces the reader to hold four
  things at once and act on none of them properly. This governs how findings, readouts, agent
  results and options are surfaced. It does not license leaving work unfinished: finish the work,
  then report it a topic at a time.

## 10. Secrets

`.env`, never committed, `.env.example` committed with empty values:

```
PREVENTIA_MODEL_PROVIDER=
OLLAMA_HOST=
OLLAMA_MODEL=
MOONSHOT_API_KEY=
ANTHROPIC_API_KEY=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_APP_SECRET=
```

If a token is ever pasted into a commit, rotate it rather than rewriting history.

## 11. Demo runbook

The patient channel is Meta's **WhatsApp Cloud API test number**. It is free, needs no business
verification, takes under 30 minutes to set up, and puts a real WhatsApp message on a real phone.
Setup, in order:

1. Create a Meta developer app, add the WhatsApp product. Meta issues a free test sender number.
2. Add up to **5 recipient numbers**. Each is verified by an OTP that arrives in WhatsApp. Ours:
   the patient-role phone, the clinician-role phone, and the developers'. The test number only ever
   talks to these 5, which is a production limitation and exactly the isolation we want for a demo.
3. **Replace the default access token immediately.** The token Meta shows you in the console expires
   in 60 minutes. Create a System User with a permanent token before demo day. This is the most
   likely way the demo dies on camera.
4. Point the webhook at a public HTTPS URL (tunnel from localhost) and complete the verification
   handshake.

**The rule that shapes the video:** free-form messages only flow inside a 24-hour window that opens
when the *recipient* messages us first. Outside it, only pre-approved templates. So the recording
opens with the patient-role phone sending a message, which is honest anyway, since the story is a
patient answering a daily check-in. Every further patient reply refreshes the window.

**Record the video on 5 August, not on the 6th.** A dead venue network on demo day must cost us
nothing.

**Backup ladder**, in order of preference: Cloud API test number, then Twilio Sandbox (five minutes,
recipient texts a join code, no Meta app, but a US sender number and sessions that expire after
three days), then the local console channel with no telephony at all.

**Not an option:** driving a personal WhatsApp account through a reverse-engineered client
(whatsmeow, Baileys, or an MCP server wrapping either). It violates Meta's terms regardless of
message content, carries a real and unpredictable ban risk on a personal number, and demonstrates a
channel that could never legally carry a real patient. In a lab judged on a pathway to adoption in
an actual health network, that is a hole a management-criteria judge will find.

## 12. Definition of done for the Lab

The video and the pitch must show, in this order:

1. An older adult answering a daily check-in in natural Chilean Spanish, on a real phone.
2. A symptom mentioned in passing, not in answer to a direct question, being picked up.
3. The traffic light turning red, and the reason why, stated in one line.
4. The escalation arriving in the clinician's triage queue with the longitudinal summary already
   assembled.
5. A live demonstration that the agent refuses to diagnose or change a dose, and a test suite that
   proves the refusal is enforced in code rather than requested in a prompt.

If something on this list is not working by the afternoon of day 2, cut scope elsewhere. This list
is the pitch.
