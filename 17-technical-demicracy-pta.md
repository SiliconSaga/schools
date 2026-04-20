---
layout: default
title: "PTA Coordination Layer"
nav_exclude: true
---

# Technical Design: Demicracy PTA Coordination Layer

*Architecture for Skill Inventories, Proposal Workflows, Commitment Tracking, and Integration with OpenCollective*

> **Document Type:** Technical design plan -- for platform builders, not the
> school board. This document describes how the Demicracy platform serves PTA
> coordination needs. It is not part of the printed whitepaper.
> **Audience:** Developers, Demicracy contributors, technical PTA volunteers
> **Prerequisite reading:**
> [Module 13 (PTA Coordination)](15-pta-coordination),
> [Module 14 (PTA+OpenCollective)](16-pta-opencollective)

---

## System Context

The PTA coordination layer sits within Demicracy's Organization & Governance tier,
leveraging the existing Backstage portal and Forgejo-based process codification.
It integrates with external services (OpenCollective, Matrix, existing PTA tools)
rather than replacing them.

```
┌─────────────────────────────────────────────────────────────┐
│                    PTA Member (Browser)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Backstage Portal                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Skill        │ │ Proposal     │ │ Commitment           │ │
│  │ Inventory    │ │ Board        │ │ Tracker              │ │
│  │ Plugin       │ │ Plugin       │ │ Plugin               │ │
│  └──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘ │
│         │                │                     │             │
│  ┌──────▼────────────────▼─────────────────────▼───────────┐ │
│  │              Backstage Catalog (unified data model)     │ │
│  └──────┬────────────────┬─────────────────────┬───────────┘ │
└─────────┼────────────────┼─────────────────────┼─────────────┘
          │                │                     │
  ┌───────▼──────┐ ┌───────▼──────┐ ┌────────────▼───────────┐
  │   Forgejo    │ │ OpenCollective│ │    Matrix              │
  │ (proposals   │ │ (finances)    │ │ (notifications,        │
  │  as repos)   │ │              │ │  coordination chat)    │
  └──────────────┘ └──────────────┘ └────────────────────────┘
```

## Component 1: Skill & Resource Inventory

### Data Model

The inventory is modeled as Backstage **Components** of a custom kind
(`kind: CommunityMember`), registered in the catalog.

```yaml
# Example catalog entry (stored in Forgejo, synced to Backstage)
apiVersion: backstage.io/v1alpha1
kind: CommunityMember
metadata:
  name: parent-jane-doe
  title: Jane Doe
  annotations:
    demicracy.io/privacy-level: "coordinators-only"  # or "public"
    demicracy.io/school: "washington-elementary"
    demicracy.io/joined: "2026-04-01"
spec:
  type: volunteer
  skills:
    - category: professional
      items:
        - grant-writing
        - nonprofit-accounting
    - category: practical
      items:
        - photography-dslr
        - electric-leaf-blower
  availability:
    hours_per_month: 8
    preferred_days: [saturday, sunday]
    preferred_projects: [grant-writing-corps, open-image-project]
  resources:
    - type: equipment
      item: "Canon EOS R6"
      available_for_loan: true
    - type: equipment
      item: "EGO Power+ 650 CFM blower"
      available_for_loan: true
```

### Privacy Architecture

Aligns with Demicracy's SSI (Self-Sovereign Identity) layer:

- **Public fields:** skill categories, availability ranges, school affiliation
- **Coordinator-visible:** name, contact info, specific equipment details
- **Private (never stored):** address, employment details, financial info

Members control their own entries. Coordinators search by skill/availability
but only see identity details for people who have opted in. This uses
Demicracy's existing Hyperledger Indy verifiable credentials -- a member can
prove "I have photography equipment" without revealing their name until they
choose to.

### Search & Matching

Backstage's existing catalog search + custom filters:

```
GET /api/catalog/entities?filter=kind=CommunityMember&filter=spec.skills.items=grant-writing
```

When a new project creates a volunteer need, the system queries the inventory
and notifies matching members via Matrix. The coordinator sees: "12 members match
this skill. 7 are available this month. 3 have expressed interest in this project."

### Onboarding Flow

For the immediate deployment (pre-full-platform):

1. Google Form → structured data → CSV import into Backstage catalog
2. Members can update via a simple web form that writes to their catalog entry
3. Coordinators use Backstage search UI

For the full Demicracy deployment:

1. Member creates SSI identity (Hyperledger Indy wallet)
2. Attests skills and resources as verifiable credentials
3. Catalog entry auto-populates from credentials
4. Privacy controls enforced cryptographically, not just by policy

## Component 2: Proposal & Review Workflow

### Mapping to Forgejo

Demicracy already codifies governance processes as Git repos. PTA proposals map
naturally:

| PTA Concept | Forgejo Concept |
|-------------|-----------------|
| New proposal | New Issue (with structured template) |
| Discussion | Issue comments (threaded) |
| Revised proposal | Pull Request against a proposal document |
| PTA board review | PR review with approve/request-changes |
| Adopted proposal | Merged PR → immutable record |
| Rejected proposal | Closed PR with documented reasoning |
| Community endorsement | Reactions / linked "support" comments |

### Proposal Template

```markdown
---
title: [Proposal Title]
author: [Name or anonymous]
date: [ISO 8601]
category: [bridge-grant | revenue | maintenance | governance | other]
estimated_cost: [$ amount or "volunteer-only"]
volunteer_needs: [number of people, skills required]
timeline: [implementation timeline]
school: [specific school or "district-wide"]
---

## Problem
[What specific problem does this address?]

## Proposed Solution
[What do you want to do?]

## Cost & Funding
[How much does it cost? Where does the money come from?]

## Volunteer Requirements
[What skills and time commitments are needed?]

## Success Criteria
[How do we know it worked?]

## Risks & Mitigations
[What could go wrong? How do we handle it?]
```

### Review SLA

The PTA board commits to responding to proposals within a defined timeframe:

- **Acknowledgment:** within 48 hours (automated)
- **Initial review:** within 1 week (at least one PTA board member comments)
- **Decision:** within 2 weeks of submission (approve, request revision, defer
  with explanation, or reject with documented reasoning)

The SLA is itself a governance document stored in the Forgejo repo -- version-
controlled, publicly visible, and amendable through its own PR process.

### Integration with Commitment Tracking

When a proposal is approved, it automatically creates a project in the
Commitment Tracker (Component 3) with the volunteer slots defined in the proposal.

## Component 3: Commitment Tracker

### Data Model

Projects and commitments are modeled as Backstage **Resources**:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: leaf-blower-brigade-q4-2026
  title: "Leaf Blower Brigade - Fall 2026"
  annotations:
    demicracy.io/project-type: "recurring-volunteer"
    demicracy.io/source-proposal: "proposal-community-maintenance-001"
spec:
  type: volunteer-project
  owner: maintenance-working-group
  status: active
  slots:
    - id: wash-elem-oct-5
      location: "Washington Elementary - perimeter"
      date: "2026-10-05"
      time: "09:00-11:00"
      volunteers_needed: 3
      volunteers_committed:
        - member: parent-jane-doe
          status: confirmed
        - member: parent-john-smith
          status: confirmed
      volunteers_backup:
        - member: parent-alex-chen
      coverage: 67%  # 2 of 3 filled
    - id: wash-elem-oct-12
      # ...
  sla:
    target_coverage: 90%
    alert_threshold: 75%  # notify coordinators when coverage drops
    backup_activation: 48h  # activate backups 48h before if primary drops
```

### SLA Dashboard

The Backstage portal displays a real-time SLA dashboard:

```
┌─────────────────────────────────────────────────┐
│  Leaf Blower Brigade - Fall 2026                │
│  ═══════════════════════════════════════════     │
│  Overall Coverage: 94% ████████████████████░░   │
│                                                 │
│  Next 7 Days:                                   │
│  Oct 5 - Washington Elem    ██████░░  67% ⚠     │
│  Oct 7 - Lincoln Middle     ██████████ 100% ✓   │
│  Oct 9 - Roosevelt Elem     ████████░░  80% ✓   │
│                                                 │
│  ⚠ 1 slot needs volunteer - Oct 5, 1 more needed│
│  [Notify Available Volunteers]                  │
└─────────────────────────────────────────────────┘
```

### Notification Flow (via Matrix)

```
Slot created → Matching volunteers notified
                     ↓
              Volunteer commits → Coordinator notified, coverage updated
                     ↓
     48h before event, coverage < threshold → Backup volunteers activated
                     ↓
          Event occurs → Coordinator marks attendance
                     ↓
     Follow-through data feeds into volunteer reliability scores (opt-in)
```

## Component 4: OpenCollective Integration

### API Bridge

OpenCollective provides a GraphQL API. The Demicracy platform reads (not writes)
financial data to display alongside coordination data:

```graphql
# Query project fund status
query {
  collective(slug: "washington-elementary-pta") {
    projects {
      name
      balance { value currency }
      stats {
        totalAmountReceived { value }
        totalAmountSpent { value }
        backers { total }
      }
    }
  }
}
```

### Unified Dashboard

The Backstage portal aggregates:

| Source | Data |
|--------|------|
| OpenCollective | Fund balances, contribution counts, expense history |
| Forgejo | Active proposals, review status, decision history |
| Commitment Tracker | Volunteer coverage, SLA status, upcoming events |
| Skill Inventory | Capacity summary -- total volunteers, skills available |

A PTA coordinator sees one dashboard with financial, operational, and human
resource data. A parent sees a public view showing fund progress, active
projects, and ways to contribute (money, time, or skills).

### Financial Boundaries

The integration is **read-only by design**. The Demicracy platform never touches
money. OpenCollective handles all financial transactions, tax compliance, and
receipt management. Demicracy displays the data for coordination purposes.

This separation is critical for:

- Regulatory compliance (PTA financial controls remain with OpenCollective/fiscal host)
- Trust (no custom platform handles money)
- Simplicity (financial audit trail lives in one place)

## Deployment Phases

### Phase 0: Now (pre-board-meeting, 5 days)

- Google Form for skill inventory → spreadsheet
- Simple sign-up sheet for commitment demonstration
- OpenCollective collective created with 2-3 seed projects
- Printed screenshots for the whitepaper stack

### Phase 1: Post-Meeting (1-3 months)

- Forgejo instance for proposal workflow (can use gitea.com hosted)
- Backstage catalog populated from Form data
- OpenCollective projects aligned to approved modules
- Matrix room for PTA coordination (bridged to existing WhatsApp/email groups)

### Phase 2: Integration (3-6 months)

- Backstage plugins for skill search and commitment tracking
- OpenCollective API integration for financial dashboard
- Proposal workflow templates and review SLA in Forgejo
- Public-facing portal for community visibility

### Phase 3: Full Demicracy (6-12 months)

- SSI integration for privacy-preserving volunteer profiles
- Automated matching and notification pipelines
- Cross-school federation (district PTA council as umbrella)
- Process codification: governance docs as version-controlled repos

## Relationship to Broader Demicracy Architecture

This PTA coordination layer is a **first production use case** for Demicracy's
core systems:

| Demicracy Layer | PTA Application |
|-----------------|-----------------|
| Identity & Trust (Indy/Keycloak) | Volunteer profiles with privacy controls |
| Data Sovereignty (Nextcloud) | Document storage for proposals, receipts, photos |
| Communication (Matrix) | Coordination chat, notifications, bridges to existing groups |
| Organization (Forgejo/Backstage) | Proposal workflow, catalog, dashboards |
| Social Graph (AT Protocol) | Future: cross-community process sharing |

The PTA use case validates the architecture at human scale (hundreds of parents,
not millions of users) with real stakes (children's education, community trust).
Success here is the proof that Demicracy's design works before scaling to larger
civic contexts.

---

[Back to Index](index)
