---
layout: page
title: Join the Lab
eyebrow: Get involved
prose: true
description: "How to join the BIRD Lab at UC Davis: current openings for undergraduates, graduate students, and postdocs, and what to put in a first email."
---

Thank you for being interested in joining our team!
We study birds to uncover the principles behind flight, then test which of them actually
earn a place in engineered systems or wildlife rehabilitation. 

Whether you come at flight from a **biology** (animal behavior, biomechanics, wildlife and raptor conservation) or **engineering** (aerodynamics, dynamics, controls, robotics) perspective, there's a place for your questions here.

{%- if site.assets.culture_photo and site.assets.culture_photo != "" %}
<figure class="culture-shot">
  <img src="{{ site.assets.culture_photo | relative_url }}" alt="The BIRD Lab group being playful in front of a wind tunnel" loading="lazy">
  <figcaption></figcaption>
</figure>
{% endif -%}

**What I look for:**

- **Curiosity and independence:** you'll drive your own project.
- **Willingness to grow:** both your technical and "soft" skills.
- **Care for the lab:** keeping the lab welcoming, safe, and rigorous is our first priority.

New here? Our [Lab Guide]({{ '/lab-guide/' | relative_url }}) and
[research]({{ '/research/' | relative_url }}) pages show how we actually work. Consider giving these a
glance before you reach out.

## Openings right now

<div class="grid grid-3 openings">
{%- assign ug = site.data.openings.undergrad -%}
<div class="card">
{%- if ug.open %}<span class="status status--active">{{ ug.open_note }}</span>{% else %}<span class="status status--paused">{{ ug.closed_note }}</span>{% endif %}
<h3>Undergraduates</h3>
<p>One or two junior/senior students each quarter at UC&nbsp;Davis. <strong>All majors welcome.</strong></p>
<p>Most undergraduate research begins as volunteer or for-credit work. Paid positions occasionally open when funding allows, and I'll help you apply for your own funding (URC, CITRIS, etc.).</p>
<a class="btn btn--primary" href="{{ site.undergrad_form_url }}">Start the interest form &rarr;</a>
</div>
{%- assign grad = site.data.openings.graduate -%}
<div class="card">
{%- if grad.open %}<span class="status status--active">Now recruiting</span>{% else %}<span class="status status--paused">Open via fellowship</span>{% endif %}
<h3>Graduate students</h3>
<p>{% if grad.open %}{{ grad.open_note }}{% else %}{{ grad.closed_note }}{% endif %}</p>
<p>I advise in <a href="https://mae.ucdavis.edu/graduate">Mechanical &amp; Aerospace Engineering</a> (MS &amp; PhD) and <a href="https://anb.ucdavis.edu/">Animal Behavior</a> (PhD).</p>
<a class="btn btn--primary" href="mailto:{{ site.lab.pi_email }}?subject={{ 'Prospective graduate applicant - BIRD Lab (UC Davis)' | uri_escape }}&body={{ site.data.openings.email_body | uri_escape }}">Email me &rarr;</a>
</div>
{%- assign postdoc = site.data.openings.postdoc -%}
<div class="card">
{%- if postdoc.open %}<span class="status status--active">Now recruiting</span>{% else %}<span class="status status--paused">Open via fellowship</span>{% endif %}
<h3>Postdocs</h3>
<p>{% if postdoc.open %}{{ postdoc.open_note }}{% else %}{{ postdoc.closed_note }}{% endif %}</p>
<a class="btn btn--primary" href="mailto:{{ site.lab.pi_email }}?subject={{ 'Prospective postdoc - BIRD Lab (UC Davis)' | uri_escape }}&body={{ site.data.openings.email_body | uri_escape }}">Email me &rarr;</a>
</div>
</div>

<p class="muted u-fs-sm"><strong>Undergraduates take part as volunteers or for EME/EAE 199 credit.</strong> Participation is voluntary and flexible; many find around 8 hours a week works well, but you set what fits alongside your coursework. Coursework always comes first: research should add to your progress, not substitute for it. You may take EME or EAE 199 with written permission. The number of 199 credits is set by the hours committed. 199 students must give a short presentation at the end of the quarter. 199 students are usually previous lab volunteers, so volunteering is the normal first step.</p>

<p class="muted u-fs-sm"><strong>Funding your own spot?</strong> Browse our <a href="{{ '/lab-guide/funding-applications/' | relative_url }}">curated list of fellowships &amp; scholarships</a>, with options for undergraduates, graduate students, and postdocs.</p>

## Applying for a graduate spot

Two things happen in parallel, and the timing matters:

1. **Email me in early fall.** I start meeting prospective students then, so reaching out early is how you're considered for *the lab* specifically.
2. **Apply to the UC&nbsp;Davis graduate group** by its [December priority deadline](https://grad.ucdavis.edu/program-application-deadlines). Admissions, requirements, and funding are run by the program, not by me: apply through [Mechanical &amp; Aerospace Engineering](https://mae.ucdavis.edu/graduate) (MS &amp; PhD) or [Animal Behavior](https://anb.ucdavis.edu/) (PhD).

I don't expect a particular background or checklist of skills. Genuine curiosity, a drive to advance science, and the persistence to see it through matter far more.

## What to put in a first email

A short, specific note is all I need, and it helps me write you a real reply:

- **Who you are:** program or year, and a line of background.
- **Why this lab:** a [project]({{ '/research/' | relative_url }}) or [paper]({{ '/publications/' | relative_url }}) that caught your eye.
- **What you'd like to build or learn** here.
- **Your timing**, with a CV and unofficial transcript attached.

I read every email and reply within about two weeks. If you don't hear back, a friendly
nudge is welcome. It's kind to open with "Dr.&nbsp;Harvey"; we're on first names once
you've joined. If it looks like a fit, we'll set up a short Zoom, and that's a two-way
conversation: you're deciding whether the lab is right for *you*, too.

<p class="muted u-fs-sm">First time reaching out to a research lab? Two guides I like:
<a href="https://sites.google.com/view/apply-academic-positions/graduate-student?authuser=0">applying to academic positions</a>
and <a href="https://ugr.ue.ucsc.edu/email">how to email a professor about research</a>.
Wondering what grad school at Davis is actually like (cost of living, campus life, support)?
UC&nbsp;Davis <a href="https://grad.ucdavis.edu/prospective-students">Graduate Studies for prospective students</a> covers it.</p>
