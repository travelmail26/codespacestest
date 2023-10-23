import requests


# Your OpenAI API key
API_KEY = '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'

# Placeholder for extended text, like reports and articles


instructionset = """
You are a reporter and will write out a short journalistic piece based on the prompt
"""

def openAI(prompt):
    # Compose the input for the API
    messages = [
        {"role": "system", "content": "You are going to write a journalistic article."},
        {"role": "system", "content": instructionset},
        {"role": "system", "content": extended_context},
        {"role": "user", "content": prompt}
    ]

    # Make the API call
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': 'gpt-3.5-turbo-16k', 'messages': messages},
        timeout=30
    )

    print ('DEBUG: response code', response.status_code)

    # if response.status_code == 200:
    #     response_data = response.json()
    #     message_content = response_data.get('choices', [{}])[0].get('message', {}).get('content', "Sorry, I couldn't process your request.")
    #     return message_content
    
    # Extract the assistant's message from the API response
    response_data = response.json()
    message_content = response_data.get('choices', [{}])[0].get('message', {}).get('content', "Sorry, I couldn't process your request.")
    return message_content

# Example usage
user_input = "Write an 200 word news article about the state of congressional policy for psychedelics complete with background on current state policies"



extended_context = """
Here are a few articles written about the current state of 
psychedelics policy in the United States. Draw from each one when writing your own article from the prompt

***Article 1 below:




EXECUTIVE SUMMARY
The COVID-19 pandemic has exacerbated a national mental-health crisis in the United
States. Drug overdose deaths have climbed rapidly over the past 20 years, and suicide rates
have gradually increased.
Psilocybin and other psychedelics have shown great promise in treating mental-health
conditions, but their use is severely limited by legal and social obstacles. Over the past
decade, medical and scientific communities have increasingly recognized the potential of
psychedelic therapies for the treatment of intractable mental health conditions. Legal and
logistical barriers to innovation have remained as the range of potential uses for
psychedelic substances has expanded. Accessing a reliable, high-quality supply of
experimental drugs for clinical trials has been a major obstacle.
Psychedelics have the potential to be more effective than conventional drugs now being
used to treat a range of mental health disorders. Current drug options frequently have
efficacy rates in the low teens.1
The U.S. Food and Drug Administration (FDA) began expediting psilocybin research and
approval by designating it as a "breakthrough therapy" in 2019 after the agency recognized

If research shows SSRIs and psychedelics do not negatively interact
when administered together, psychedelic-assisted therapies could
transform from stand-alone treatments to complementary treatments,
which would expand their markets.
Many of the people who are helped by psychedelic-assisted therapies are also taking other
drugs, like selective serotonin reuptake inhibitor (SSRI) antidepressants, for relief. It's
important to learn how these common drugs and psychedelics interact with each other. If
research shows SSRIs and psychedelics do not negatively interact when administered
together, psychedelic-assisted therapies could transform from stand-alone treatments to
complementary treatments, which would expand their markets. This could allow
participants in the therapy to slowly taper off SSRIs as the longer lasting effectiveness of
psychedelic-assisted therapies take hold so that these individuals do not suffer from rapid
withdrawal symptoms. Alternatively, there may be some scenarios in which a patient and
their doctor wish to continue SSRI usage alongside psychedelic-assisted therapies,
although many patients may hope psychedelic therapies can enable them to avoid the need
for continual, ongoing medication.
Oregon, Colorado, and Washington, D.C., are already taking strides toward establishing
regulatory frameworks that allow licensed professionals to administer psilocybin therapy
even without FDA approval of these treatments. Lawmakers in other states have proposed
comparable legislation in rapid succession, indicating that state-licensed psychedelic
therapies are likely to continue expanding. These regulatory regimes could increase the

BACKGROUND
There are a variety of biological ("pharmacotherapy") and psychological ("psychotherapy")
treatment options for depression, each of which focuses on a distinct aspect believed to be
the primary pathological cause under its own unique theoretical framework.4 Commonly
used pharmaceutical treatments are mostly based on the idea that depression is brought on
by a lack of monoamine neurotransmitters, including serotonin (5-HT), dopamine, and
norepinephrine and their receptors, which are crucial for controlling mood, arousal, and
memory.
Different forms of antidepressants, such as selective serotonin reuptake inhibitors (SSRIs) or
monoamine-oxidase inhibitors, are thought to lessen depression symptoms by raising these
neurotransmitter levels to differing degrees.5 Antidepressants,6 despite helping only a
portion of patients diagnosed with severe depression, can have serious side effects,
4 Susan Nolen-Hoeksema, “Mood Disorders and Suicide,” In: Abnormal Psychology. Boston: McGraw-Hill
(2017). p. 172-213.
5 Stephen M. Stahl, “Stahl′s Essential Psychopharmacology: Neuroscientific Basis and Practical Applications
(Fourth Edition),” Cambridge University Press (2013), 8(1):146-50.
6 Jay C. Fournier et al. “Antidepressant Drug Effects and Depression Severity: A Patient-Level MetaAnalysis.” Journal of the American Medical Association, Vol. 303, No. 1 (2010), pp. 47-53. Available at:
https://pubmed.ncbi.nlm.nih.gov/20051569/.
PART 1 
MODERNIZING PSILOCYBIN POLICY TO IMPROVE MENTAL HEALTH OUTCOMES
Modernizing Psilocybin Policy To Improve Mental Health Outcomes
2
including sexual dysfunction and cardiovascular hazards.7 In addition, there is a
considerable risk of relapse after stopping antidepressants, which is why they are
frequently taken on a long-term basis.8
Antidepressants, despite helping only a portion of patients diagnosed
with severe depression, can have serious side effects, including sexual
dysfunction and cardiovascular hazards.
Interpersonal therapy and cognitive-behavioral therapy (CBT), both based on many
psychosocial theories that aim to change one's behavioral and cognitive biases through
regular therapy sessions, are two types of psychotherapy used to address depression.
Although there are significant reductions in depression symptoms,9 recurrence and dropout
rates are still rather high.10 Because of this, typical pharmaco- and psychotherapies for
major depressive disorder (MDD) are usually combined, which has been proven to be more
successful than either method alone.11 Even so, a sizable share of MDD patients never fully
recover, including roughly 75percent after 8 weeks and around 25percent after 24 weeks of therapy.12
In response to the limitations of traditional pharmacotherapeutic or psychotherapeutic
treatments, there has been a rapidly growing interest in the potential use of psychedelic
compounds to address depression and various other mental health conditions, and some


have proposed psilocybin as a promising alternative treatment method. Psilocybin is a
naturally occurring hallucinogenic substance present in some types of mushrooms. Many
cultures throughout history have used it to elicit altered states of consciousness for
ceremonial, therapeutic, medical, and spiritual purposes.
13 Psilocybin is currently listed as a
Schedule I substance under the Controlled Substance Act and banned under federal law in
the United States.14 Meanwhile, a growing body of data suggests that psilocybin use may
have therapeutic advantages.
A 2004 pilot study from the University of California, investigating the possibility of
psilocybin treatment in patients with advanced-stage cancer, reignited interest and
significantly renewed efforts in psilocybin research, ushering in a new era in the
investigation of psychedelic therapy. Since then, much has been discovered about the
chemical characteristics of psilocybin as well as its possible therapeutic applications.15
Psilocybin has low physiological toxicity, low risk of abuse or
addiction, safe psychological reactions, and no linked persistent
harmful physiological or psychological effects during or after use.
Generally, psilocybin is said to have the best safety profile of any psychedelic substance.
Psilocybin has low physiological toxicity, low risk of abuse or addiction, safe psychological
reactions, and no linked persistent harmful physiological or psychological effects during or
after use, according to thousands of years of anecdotal data as well as contemporary
scientific investigations. Psilocybin overdose is extremely uncommon.

The FDA certifies a drug as a breakthrough therapy if preliminary clinical data
indicates that it may significantly outperform current treatments. 17 In the space of one
year, the FDA designated psilocybin therapy, which is now being evaluated in clinical trials,
as a "breakthrough therapy" for the treatment of two different forms of depression. This
designation is intended to speed up the customarily drawn-out process of drug
development and evaluation. According to the FDA, it is normally requested by a
pharmaceutical company and only approved when early research indicates the drug may be
a far superior treatment option to those currently on the market.
The FDA‘s granting of breakthrough status to psilocybin therapy is
particularly significant given that psilocybin is a Schedule 1 substance
and its manufacture and distribution is expressly forbidden under
federal law.
Psilocybin therapy received this designation in 2021 in the ongoing clinical trials being
conducted by COMPASS Pathways to examine psilocybin's potential to treat severe
depression in patients whose condition has not improved after receiving two
antidepressant medications.18 The FDA‘s granting of breakthrough status to psilocybin
therapy is particularly significant given that psilocybin is a Schedule I substance and its
manufacture and distribution is expressly forbidden under federal law.
Dr. Matt Johnson, a prominent scientist at Johns Hopkins University’s psychedelics research
center and leading expert, claims psilocybin has some abuse potential and risk; however,
there isn't much evidence to support it causing physical dependence. Generally, it can be
used safely when administered under medical supervision.19 However, because the

medication tends to intensify the current affective state, unpleasant effects, such as anxiety
or psychotic reactions, may happen when psilocybin is delivered in a setting that could
trigger negative emotional sentiment.20 Researchers like Johnson argue it is crucial to
provide patients with psychological support and environments that make them feel
comfortable and safe in order for psilocybin-assisted therapy to achieve its intended
benefits.
Psilocybin offers promise for a range of additional disorders, including
anxiety in terminal illness, neurodegenerative disease, obsessivecompulsive disorder, and drug dependency, aside from its potential
therapeutic efficacy in treating depression.
Psilocybin initiates long-lasting favorable changes in well-being, attitude, and personality
with just one administration if certain measures are taken.22 Psilocybin offers promise for a
range of additional disorders, including anxiety in terminal illness, neurodegenerative
disease, obsessive-compulsive disorder, and drug dependency, aside from its potential
therapeutic efficacy in treating depression.23 Although preliminary, these promising findings
are mostly based on a limited number of small-scale controlled trials, limiting the
widespread acceptance for use in clinical practice.

for using psychedelics to treat a range of mental health conditions. These businesses
contend that patents are required to protect their investments in both drug discovery and
commercialization, which involve costly clinical studies and other criteria to win FDA and
other regulatory approval as well as support from the medical community. Pharmaceutical
companies are incentivized to develop drugs that treat widely held conditions so they can
gain the customer base necessary to recover the costs of taking a product through FDA
trials, which regularly add up to more than $1 billion.50 Drug companies have to sell at
monopoly prices over a prolonged period to recover these costs and make the risk
worthwhile.
…drug developers like COMPASS Pathways have applied for patents
on psilocybin chemicals and procedures for using psychedelics to
treat a range of mental health conditions.
At the same time, stakeholders, including patient activists, scientists, journalists, attorneys,
and indigenous communities have criticized the sudden interest in patenting
psychedelics.51 Some contend that patenting psychedelics constitutes "biopiracy," or the
appropriation of indigenous communities' traditions.52 Others contend that patents turn a
select few businesses into the industry's gatekeepers, which might limit innovation, impede
research, and prevent access to necessary treatments.
These issues do not apply only to psychedelics. Similar discussions have been sparked by
patents on genetic technologies, cancer treatments, and other innovations.53 However,
several characteristics of psychedelics, such as their extended and complex history, create
special considerations that might complicate issues with medical product patenting.

Two prerequisites for patentability are novelty and non-obviousness. While a mushroom
may not be able to be legally patented, due to its natural occurrence and existing
availability to the public, extracts of psilocybin or slight variations on its chemical structure
may offer novelty. These distinctions undergird the U.S. Patent and Trademark Office’s
decision to grant some psychedelic patents.54
The threshold for acquiring a patent is much lower than for gaining
FDA approval, which requires clinical trial-based evidence of safety
and efficacy.
The threshold for acquiring a patent is much lower than for gaining FDA approval, which
requires clinical trial-based evidence of safety and efficacy. Patent applicants need merely
demonstrate that a person with understanding in the relevant technological field may
potentially create and use the invention after reading the patent application. The patent
office does not require that the approach be fully developed or that its safety and
effectiveness be demonstrated.
The medical product patent environment can be described as a thicket: a complex network
of interlocking patent rights that prevents rivals from entering. Patent thickets are formed
when patent holders pepper the field with multiple patents on the same or nearly related
items, discouraging potential researchers and manufacturers from entering the sector
entirely for fear of being sued for infringement or having to pay exorbitant license fees to
patent holders.55
Rules for newness and non-obviousness in U.S. patent law stricter could prevent small
changes to existing inventions from being classified as patentable innovations because
they are not substantially novel. Giving patents on these small changes adds to the patent
thicket and makes people less likely to try new things, which could slow scientific and
technological progress.

Despite criticisms, however, the market is already addressing many of these concerns.
Individuals have contributed to nonprofit research organizations like Usona and B. More,
whose inventions enter the public domain. Other companies have made or may make
"patent pledges" for medical products, essentially waiving their intellectual property claims
over those products.56 These patent pledges sometimes can be confusing in court,
considering many parties may attach stipulations to their agreements. However, the market
process has already produced a range of outcomes in which psychedelic-assisted therapy
would be within the public domain due to private philanthropy and others in which
companies seek to fully recoup the costs imposed by pharmaceutical regulation.
Controlled substances. Most psychedelics, excluding ketamine, are Schedule I controlled
substances because they have no recognized medical value and a significant misuse
potential, according to the DEA.57 Attempted commercialization of any Schedule I drug
includes substantial legal and financial risk, creating market uncertainty and discouraging
risk-averse investors. The remaining risk-tolerant investors are likely to coalesce into
relatively few research firms, leading to a concentration of patent monopolies. Schedule I
classification limits who has distribution and sale access to companies with large funding.
Hence, psychedelic market concentration and patent holdings are in the hands of a only
few companies.58 Essentially, firms that can afford to conduct their research and
development overseas are the ones that overcome current federal policies on psychedelics.
Essentially, firms that can afford to conduct their research and
development overseas are the ones that overcome current federal
policies on psychedelics.

EMERGING LEGAL
FRAMEWORKS
Until 2020, the manufacturing and consumption of psilocybin was illegal under federal law
and the laws of all 50 states. But in November 2020, Oregon voters enacted the first statelevel program designed to authorize professionally facilitated psilocybin services via
Measure 109. Measure 109 created a program for administering psilocybin products to
individuals aged 21 years or older through a state-regulated program that licenses
manufacturers, service centers, and facilitators.59,
60
The Oregon Health Authority (OHA) is responsible for setting up the program and making
regulations under Measure 109, expected to go live in 2023. The OHA is advised by the
Oregon Psilocybin Advisory Board (OPAB). OPAB gives recommendations to OHA based on
scientific studies and research about the safety and effectiveness of psilocybin in treating
mental health conditions. It also gives recommendations about the requirements,
specifications, and guidelines for providing psilocybin services in Oregon. OPAB is crafting a
long-term vision to ensure that psilocybin services will gain recognition as a safe,

accessible, and affordable therapeutic option for adults aged 21 and older in Oregon for
whom psilocybin may be appropriate.61
[Oregon Psilocybin Advisory Board] is crafting a long-term vision to
ensure that psilocybin services will gain recognition as a safe,
accessible, and affordable therapeutic option for adults aged 21 and
older in Oregon for whom psilocybin may be appropriate.
After participating in a preparatory session to advise a potential consumer and assess his or
her suitability—including screening for potentially adverse conditions—consumers would
be permitted to schedule an appointment in which psilocybin is administered in a clinical
setting at a licensed center under the supervision of a licensed facilitator. In accordance
with Measure 109, the Oregon Health Authority (OHA) has recently finalized a rulemaking
process to determine many of the program details, including who is qualified to obtain a
license as a facilitator, training requirements, a code of conduct for facilitators, and
guidelines for packaging, labeling, and product mix.62 The market is expected to launch in
the second half of 2023.
Measure 109 permits cities and counties to put questions on local ballots that would either
allow or restrict psilocybin service centers or manufacturing of psilocybin in unincorporated
regions under their control. The law forbids the operation of psilocybin service centers
inside the boundaries of incorporated cities.
No medical condition is required for patients seeking psilocybin services in Oregon. Psilocybin
services could help close the current gap in preventative mental healthcare because clinicaltrial participants frequently experience long-lasting sensations of well-being.63


Several other jurisdictions are reconsidering new regulatory
frameworks for psilocybin use.
Several other jurisdictions are reconsidering new regulatory frameworks for psilocybin use:
• In November 2022, nearly 54percent of Colorado voters approved Proposition 122, which
will create a regulated market for professionally facilitated psychedelic experiences
and decriminalize possession of several common psychedelic substances, starting
first with psilocybin and then moving on to mescaline, dimethyltryptamine (DMT),
and ibogaine. The law creates a new Regulated Natural Medicine Access Program
through which psychedelic professionals would be certified through state-approved
training institutes and will conduct psychedelic experiences at approved locations,
though consumers would not be able to purchase psychedelic plant medicine
directly via retail establishments.
64 The measure gives Colorado's Department of
Regulatory Agencies (DORA) broad authority to set up regulatory guidelines for
training certification, administration sites, and manufacturing.
• Initiated Ordinance 301 was passed in Denver in 2019 with 50.6 percent of the vote.
The law made the possession and use of psilocybin mushrooms by adults the lowest
priority for law enforcement in Denver and stopped the city from spending money to
enforce penalties related to them.
• Voters in Washington, D.C., approved a ballot measure in November 2020 instructing
police to regard the non-commercial distribution, production, possession, and use of
entheogenic plants and fungi as one of the lowest priorities for law enforcement.65
Through local ordinances, psilocybin has also been made legal in three additional
cities: Oakland, Santa Cruz, and Ann Arbor.
A combination of bottom-up grassroots activism and top-down regulatory reform may lead
to a reinforcing loop that eventually broadens access to psychedelics in terms of both
geography and eligibility requirements.46 Multiple states are considering legislation in 2023
to decriminalize the possession and use of psilocybin and other psychedelics or to establish
legal, regulated markets like Oregon. We expect the current pattern to continue, in which
some psychedelics companies openly declare their intentions to enter these regionally
legalized markets, while others intend to avoid doing so as long as psychedelics are still
illegal at the federal level.67
A combination of bottom-up grassroots activism and top-down
regulatory reform may lead to a reinforcing loop that eventually
broadens access to psychedelics in terms of both geography and
eligibility requirements.


***article 2 starts here

The U.S. House of Representatives on Thursday approved several marijuana reform amendments as part of a large-scale defense bill, including proposals to protect banks that work with state-legal cannabis businesses and allow U.S. Department of Veterans Affairs (VA) doctors to issue medical marijuana recommendations.

A total of nine drug policy measures passed the chamber as part of the National Defense Authorization Act (NDAA) this week, after being made in order for floor consideration by the Rules Committee on Tuesday.

On Wednesday, the House first approved a bipartisan pair of psychedelics research amendments, as well as another measure requiring a military study into marijuana-related enforcement discrimination in the armed services. Those were part of the first en bloc package of measures that were taken up on the floor.

Subsequent packages contained a wide range of cannabis proposals. One amendment from Rep. Ed Perlmutter (D-CO) that advocates and stakeholders have been monitoring especially closely contains the language of the Secure and Fair Enforcement (SAFE) Banking Act, which would protect financial institutions that service state-legal marijuana businesses from being penalized by federal regulators.

Perlmutter discussed the measure in the Rules Committee on Tuesday, arguing that it was germane to the defense legislation because it could help combat international drug trafficking, which poses a national security risk. The House adopted the amendment as part of last year’s NDAA, but the Senate didn’t go along so it was not included in the final bill.

The congressman also tried getting marijuana banking reform included in a large-scale manufacturing bill that’s in bicameral conference, but leadership agreed to exclude the language, prompting him to pursue another vehicle.

Meanwhile, an amendment from Reps. Earl Blumenauer’s (D-OR) and Brian Mast (R-FL) to codify that VA doctors can discuss and issue recommendations for medical cannabis to veterans also passed the House.

In a Dear Colleague letter that was shared with Marijuana Moment, Blumenauer and Mast talked about the unique therapeutic potential of cannabis for veterans suffering from PTSD and argued that current VA policy prohibiting doctors from issuing recommendations “forces veterans to seek care outside of the VA to receive opinions and recommendations on this care option.”

“VA physicians should not be denied the ability to offer a recommendation that they think may meet the needs of their patients,” they wrote. “Veterans should not be forced outside the VA system to seek treatment that is legal in their state.”

A bipartisan group of lawmakers, including Blumenauer, separately filed an amendment to an appropriations minibus on Wednesday that would block VA from preventing military veterans from using medical cannabis while allowing its doctors to fill out recommendations for patients who want to participate in state programs.

Rep. Nancy Mace (R-SC) had an amendment to NDAA adopted that similarly provides VA doctors with that authority, but it goes further by prohibiting federal employers from discriminating against veterans who use, or have used, marijuana.

The House additionally approved a revised measure from Rep. Katherine Clark (D-MA) that expresses the sense of Congress that VA should not deny home loans to veterans because they derive income from a state-legal marijuana business. The proposal was initially introduced as an outright prohibition of such denials, but was changed to a nonbinding form.

Rep. Alexandria Ocasio-Cortez (D-NY) secured two drug policy amendments to the NDAA. One that passed on Wednesday builds on a measure from Rep. Seth Moulton (D-MA), requiring the Department of Defense (DOD) to study marijuana as an opioid alternative in the treatment of service members with post-traumatic stress disorder (PTSD), traumatic brain injuries and severe pain. Ocasio-Cortez’s proposal widens the scope of that research to include psilocybin and MDMA.

Then on Thursday, the congresswoman’s amendment to prevent the use of funds for aerial fumigation on drug crops in Colombia was adopted. The practice has been widely criticized by reform and human rights advocates.

The other psychedelics amendment that cleared the chamber on Wednesday was sponsored by Rep. Dan Crenshaw (R-TX). It would allow the secretary of defense to approve grants for research into the therapeutic potential of certain psychedelics such as MDMA, psilocybin, ibogaine and 5–MeO–DMT for active duty military members with PTSD.

Notably, an earlier, identical version of the was not made in order for the floor as part of last year’s NDAA, signaling that attitudes toward psychedelics have shifted in Congress over recent months.

The House on Wednesday also passed a measure from Rep. Rashida Tlaib (D-MI) that would require DOD to study the “historically discriminatory manner in which laws related to marijuana offenses have been enforced, the potential for the continued discriminatory application of the law (whether intentional or unintentional), and recommendations for actions that can be taken to minimize the risk of such discrimination.”

Finally, lawmakers passed an amendment on Thursday that was filed by Rep. Mikie Sherrill (D-NJ). It seeks to eliminate the federal sentencing disparity between crack and powder cocaine.

Lawmakers who sponsored the reforms praised their inclusion in NDAA.

“It’s time to get this done—and I will pursue any and all legislative avenues to do so,” Perlmutter said of his banking measure in a press release. “This is yet another opportunity for the Senate to advance common sense cannabis reforms starting with access to the banking system. I’m calling on them to take action for the safety of our communities and success of Veteran- and minority-owned businesses across the country.”

Meanwhile, the co-chairs of the Congressional Cannabis Caucus—Blumenauer and Mast, along with Reps. Barbara Lee (D-CA) and Dave Joyce (R-OH), released a joint statement saying that “the need to establish a more rational approach to federal cannabis policy has never been greater.”

“More than 91 percent of the American public live in states where adult use of cannabis is legal in some forms. Yet outdated and archaic federal regulations on the sale, distribution, and ability to access basic economic services continue to disproportionally harm countless communities, including our veterans,” they said, adding that the passage of the new provisions is “a significant step in remedying the federal government’s failed approach to cannabis through commonsense, bipartisan policy.”

The Perlmutter, Blumenauer and Clark measures  on banking and veterans were adopted as part of an en bloc package with dozens of other amendments by a roll call vote of 277-150, and the Ocasio-Cortez proposal on drug crop fumigation was included in another group that passed with a 330-99 vote. All of the other amendments were adopted in separate packages via voice votes.

What remains to be seen is which, if any, of these amendments makes it through conference after the Senate advances its version of NDAA. The chamber has generally been viewed as a barrier to enacting drug policy reform, especially with Republican minority leadership frequently challenging amendment germaneness.

***article 3:


"""

response = openAI(user_input)
print(response)