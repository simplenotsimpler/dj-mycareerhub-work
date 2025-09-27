# Django MyCareerHub

Django-based full-stack site that provides a single source of truth for my career data. It is a minimally viable product (MVP).

## Live Site

TBD

## Apps

- **Common:** This houses utilities that are shared across the various apps.
- **Core:** This is the repository for basic data such as my demographics, complete work history, complete education histry, skills, etc.
- **Reports:** These are printable PDF documents of the work history, education history, etc. that can be used when filling out job sites such as LinkedIn and Indeed as well as applications either online or in person.
- **Resume:** This allows me to generate resumes in PDF and Word form by selecting various details from the core data.
- **Portfolio:** This allows me to generate a portfolio site based on my selections of various details from the core data and combines this with my pinned GitHub repos.

## Details

- Intended audience is for a single fellow developer or IT person who knows how to code. Hence at this time, it uses a singleton pattern for the user demographic data.
- Because it is an MVP, it makes heavy use of the Django admin interface, i.e. the aesthetics of the backend are minimal. The goal is the data structure and basic functionality. I did not use an admin template as I found these are either not sufficiently kept up to date, often did not meet miniml accessibility concerns (semantic HTML), and thus weren't worth adding an extra dependency and potential security risk.
- Resume format is strictly ATS-compliant. Hence, this not concerned with having multiple templates.
- Portfolio is the public facing part of the site.
- Because I am the only user logging in, I have opted to keep the authentication simple and secure the site in other ways.
- ChatGPT has been used for research and assisting with code development to solve specific problems. 

## Why Django?

- JavaScript framework fatigue. I'm honestly tired of how JavaScript is always coming out with new frameworks.
- React is overkill for the minimal front-end that I need as I do not have that much interactivity.
- Not a fan of React server components, that Next.js relies on a particular vendor so much (whom I'm not fond of either), or that the server components are to tightly integrated with Next.js and this vendor.
- Prefer to host everything on the same server in a single repository. I have found that the microservice mentality adds unnecessary complexity for this use case.
- Lack of standards in the JavaScript ecosystem.
  - It seems that you always have to build an admin interface and authentication from scratch even if you use a tool like React-admin.
  - If you do use a tool like React-admin, then you have to learn it's nuanced syntax. Granted the Django admin interface is slow on updating to modern styling, but it has solved the core problems in a complete ecosystem that while opionated allows for flexible adaptation. (I'm looking forward to the updates coming in newer versions of Django.)

# License

This project is [MIT licensed](./LICENSE).
