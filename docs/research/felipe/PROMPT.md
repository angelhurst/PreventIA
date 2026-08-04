# Research brief, next workstreams

Same rules as `docs/research/PROMPTforANGEL.md`: research and write only, no code, no edits to
`PRD.md`, never invent a clinical fact or a figure, every non-obvious claim carries a source, and
anything needing a clinician's sign-off is marked REQUIRES CLINICAL REVIEW rather than resolved.

Workstreams 1 to 6 are complete and indexed in `docs/research/README.md`. These continue the
numbering. Both come out of the pilot flow drawn in
`docs/diagrams/2026-08-03-flujo-piloto-quinta-normal.excalidraw`, which is v0.0.1 and shows both of
these as undefined.

```
WORKSTREAMS

7. The guardian, and whether it belongs on the clinician dashboard
   New element in the flow, not yet defined anywhere in the repository. At
   enrolment the doctor designates, or does not designate, a guardian for the
   patient: a family member or a caregiver.

   What to establish, in this order:
   - Does an equivalent figure already exist in Chilean primary care, and what
     is it actually called there? Cuidador, cuidador principal, acompanante,
     apoderado, representante. Whether the PSCV or any MINSAL orientacion
     tecnica records one, in what field, and who is allowed to designate it.
   - What the guardian would be allowed to receive. A third party reading a
     patient's symptoms is a different privacy question from a patient reading
     their own, and Ley 20.584 on the rights and duties of patients is the
     first place to look. Report what the law requires; do not interpret it as
     legal advice, and mark the boundary where a lawyer is needed.
   - Whether designating a guardian is a setting on the clinician dashboard, a
     field captured at enrolment, or both, and whether it can change afterwards
     without a new consent.
   - What, if anything, it changes downstream: the frequency of the daily
     check-in, the threshold for escalating to red, or who the escalation
     reaches. REQUIRES CLINICAL REVIEW. Do not decide this; gather the options
     and their basis so the clinical teammate can.

   Open until answered: whether the guardian is a PreventIA concept at all, or
   a field the institution already holds and we should read rather than invent.

8. What the clinician dashboard must and must not contain
   The dashboard is the only surface a clinician touches, and it is the one
   piece of this system that cannot be designed once for everyone. It has to be
   studied per institution, because what a CESFAM team can act on is not what a
   hospital service or a Caja can.

   What to establish:
   - Who actually reads it in a CESFAM, and in what slot of their day. Doctor,
     matrona, TENS, encargado del programa cardiovascular. Whether the person
     who receives an alert is the same person who holds the patient's control.
   - What a clinician is already obliged to record when they act on a case, and
     whether the dashboard has to feed that record or sits beside it. REM
     returns and the rescate de inasistentes categories from workstream 3 are
     the concrete case.
   - What must NOT be on it. Anything that reads as a clinical recommendation,
     any inference presented as a finding, any field that would make the
     dashboard a parallel clinical record. Write this as an explicit exclusion
     list, because it is the part a clinical judge will test.
   - What changes between institutions and what is invariant, stated as two
     lists. The invariant part is what we build; the variable part is what a
     deployment configures.
   - Existing precedent: any triage or alert board already in use in Chilean
     APS, what it looks like, and what is known about whether it gets read.

   Deliverable is a specification of content and exclusions, not a visual
   design, and not a decision on any of it. Felipe and the clinical teammate
   decide.
```
