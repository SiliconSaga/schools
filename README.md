# Community Solutions for the School Budget Crisis

Community proposals for bridging the West Orange school budget gap through
transparency, volunteer coordination, and shared service grants.

**Live site:** [schools.siliconsaga.net](https://schools.siliconsaga.net)

## What's Here

This repo contains a Jekyll site (using [just-the-docs](https://just-the-docs.com/))
with assorted whitepaper documents covering:

- **Cost-avoidance modules** -- PTA bridge grants, community photography, volunteer
  maintenance, paraprofessional retention, health insurance transparency, open governance
- **Additional modules** -- energy/solar, cooperative purchasing, grant writing,
  student-led projects, regulatory leverage, open budget tools, PTA coordination,
  community sports partnerships
- **Tools** -- RFI templates for vendor/broker disclosure, a speech draft with
  print guide
- **Technical appendix** -- platform design for PTA coordination layer and budget
  visualization

## Building the Printable PDF

The repo includes a Python script to compile the core and supporting modules
into a single printable PDF with cover page, stripped metadata, and page footers.

```bash
# Requires Python 3 + reportlab
pip install reportlab

# Web version -- clickable links + footnotes, all modules (for digital sharing)
python build-pdf.py --web
# Output: whitepaper.pdf

# Print version -- footnotes only, core modules only (for paper handout)
python build-pdf.py --print
# Output: whitepaper-print.pdf
```

Both versions include a numbered reference section at the end. The web version
adds clickable links and includes supporting modules; the print version is
shorter and optimized for paper.

The script reads the markdown files in print order (defined in the `CORE_STACK`
and `SUPPORTING_STACK` lists at the top of `build-pdf.py`), strips Jekyll front
matter and site-only metadata blocks, and renders to a styled PDF. Edit the
file lists to change what's included.

## About the Author

Rasmus "Cervator" Praestholm -- West Orange resident, parent of three children
in the district (including a child with a paraprofessional), PTA member, and
volunteer with a local youth sports league. By profession, a software engineer.

These proposals were assembled aspirationally on behalf of the community. No
organizations have been committed to any of the ideas presented here, and no
promises are made about outcomes. The intent is to start a conversation and
demonstrate what community coordination could look like if the district is
willing to collaborate.

## Contributing

Open an [issue](https://github.com/SiliconSaga/schools/issues) with suggestions,
corrections, or additional ideas. Pull requests welcome. If you have expertise
in any of the areas covered (health insurance, grant writing, NJ school law,
fundraising, data visualization), your input would be especially valuable.

## Feedback

- **Site improvements:** [GitHub Issues](https://github.com/SiliconSaga/schools/issues)
- **School district feedback:** [West Orange feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfPpBHw2F13tZXD54vfKXXNQywjaz93KaJXdMLWG0AnE51csw/viewform)
