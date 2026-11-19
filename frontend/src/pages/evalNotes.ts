// Written by hand after reading the failures of the latest full evaluation run
// (deepseek-flash, prompt v1, 2026-11-19). Keep it in sync with backend/eval/results.json.
export const ERROR_ANALYSIS: string[] = [
  'All 11 mistakes are priority mistakes, and all of them are off by exactly one level. Category, reply language and the cited article were right for all 50 tickets, so the hard part is the impact × urgency judgement, not understanding the ticket.',
  'Same-day deadlines are under-weighted (T03, T19, T22, T45): the model rated urgency Medium when the user is blocked or has a deadline today. The prompt lists "a hard deadline today" as High urgency, but the model gives more weight to a possible workaround (for T19, using the phone).',
  'Group size is the fuzzy boundary for impact (T20, T23, T41): a whole floor and a phishing wave in Finance were rated High impact (P1) where the label says Medium (P2), and a 12-person remote team was rated Medium where the label says High. The matrix examples cover these cases, but they are not in the prompt.',
  'The rest lean towards over-escalation (T06, T24, T43, T46). For a help desk that is the safer direction, and some of these labels are debatable: a terminated employee with active access (T46) is arguably a P2 security exposure.',
  'One reply-format slip: for a Spanish ticket (T22) the model wrote priority_reason in Spanish although the prompt asks for English. The reply itself was correctly in Spanish.',
  'Labels were not changed after seeing these results. Category accuracy of 100% says more about this clean, self-written dataset than about real tickets, where several issues and noise are common.',
  'Next prompt iteration (v2): add the priority matrix examples as few-shot cases for group size and same-day deadlines, then re-run the same dataset and compare against v1.',
]
