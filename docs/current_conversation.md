Good morning, wanted to give some prep for education verification

Education verification is a long IF/Then statement by provider typeFirst thing, we need to get with the state boards to see if they will provide us a letter stating that they perform the highest level of education verification - if yes, then we can use thatFor MDs then we can use ABMS (and some DOs as well) - their board cert // we have an integration alreadyFor DOs then we can use AOA - their board cert // we have a manual/fee-based/one time usage only hereFor MDs and DOs if not their boards, then we can use AMA - we're hopefully building an integrationFor MDs and DOs if not AMA then we can use the National Student Clearinghouse - we're hopefully building an integrationFor MDs and DOs if not NSC - then we need to contact the institution directly This also follows for Residency and Fellowships where we'd have to contact the institution

This is a document by from CAQH that begins to lay this out
https://providertrust.slack.com/archives/C04NU3G8MA9/p1769433915766149

This is a document by NCQA that lays out two provider groups that need full credentialing (thus education) -
Medical Behavioral Health

Provider types on page 99
Education section starts on page 156

https://providertrust.slack.com/archives/C8JE5228K/p1765980901042559

Ideally the API Intelligence POC would inform this group on where to go to get the education verified because that would tell us what we have don't have as far as verified education elements. (example, we have all ABMS loaded today for MDs (some DOs))

Interesting crossover with the Intelligence POC. Bret mentioned having a few questions we use to tailor the POC around. Do you think something along the lines of what you mentioned above could be one of those questions?

for this ... is it more about - how we'd orchestrate this?
i'm not sure what additional we'd want to do

For this, I think it's twofold:
To your point, how would we orchestrate it? Could agents replace manual verification of credentials?

In some ways, I'm more interested in one, and the second supports the first. If Chris and the ELT are interested in Agents, we need to start building that muscle as a team (because it's a somewhat different beast than general LLMs). I see the CAQH/education piece as a means to begin exploring agentic capabilities internally.

Do you think the manual verification problem statement gives us an avenue to do that?