---
stand_alone: true
ipr: trust200902
docname: draft-toutain-lpwan-access-control-00
cat: std
pi:
  symrefs: 'yes'
  sortrefs: 'yes'
  strict: 'yes'
  compact: 'yes'
  toc: 'yes'

title: SCHC Rule Access Control
abbrev: SCHC AC
wg: lpwan Working Group
author:
- ins: A. Minaburo
  name: Ana Minaburo
  org: Acklio
  street: 1137A avenue des Champs Blancs
  city: 35510 Cesson-Sevigne Cedex
  country: France
  email: ana@ackl.io
- ins: L. Toutain
  name: Laurent Toutain
  org: Institut MINES TELECOM; IMT Atlantique
  street:
  - 2 rue de la Chataigneraie
  - CS 17607
  city: 35576 Cesson-Sevigne Cedex
  country: France
  email: Laurent.Toutain@imt-atlantique.fr
- ins: I. Martinez
  name: Ivan Martinez
  org: Institut MINES TELECOM; IMT Atlantique
  street:
  - 2 rue de la Chataigneraie
  - CS 17607
  city: 35576 Cesson-Sevigne Cedex
  country: France
  email: ivan-marino.martinez-bolivar@imt-atlantique.fr 
normative:
  RFC8824:
  RFC8341:
  I-D.ietf-lpwan-schc-yang-data-model:
informative:
  
    
--- abstract

The framework for SCHC defines an abstract view of the rules, formalized with through a YANG Data Model. In its original description rules are static and share by 2 entities. The use of YANG authorizes rules to be uploaded or modified in a SCHC instance and leads to some possible attacks, if the changes are not controlled. This document summarizes some possible attacks and define augmentation to the existing Data Mode, to restrict the changes in the rule. 

--- middle

# Introduction

# Attack scenario

A LWM2M device, under control of an attacker, sends some management messages to modify the SCHC rules in core in order to direct the traffic to another application. This can be either to participate to a DDoS attack or to send sensible information to another application. 

SCHC rules are defined for a specific traffic. An attacker changes en element (for instance, the dev UDP port number) and therefore no rule matches the traffic, the link may be saturated by no-compressed messages.




# YANG Access Control

YANG language allows to specify read only or read write nodes. NACM {{RFC8341}} extends this by allowing users or group od users to perform specific actions.

This granularity do not fit this the rule model. For instance, the goal is not to allow all the field-id leaves to be modified. The objective is to allow a specific rule entry to be changed and therefore some of the leaves to be modified. For instance an entry with field-id containing Uri-path may have his target-value modified, as in the same rule, the entry regarding the app-prefix should not be changed. 

The SCHC access control augments the YANG module defined in {{I-D.ietf-lpwan-schc-yang-data-model}} to allow a remote entity to manipulate the rules. Several levels are defined.

  * in the set of rules, it authorizes or not a new rule to be added .
  * in a compression rule, it allows to add or remove field descriptions.
  * in a compression rule, it allows to modify some elements of the rule, such as the target-value, the matching-operator or/and the comp-decomp-action and associated values.
  * in a fragmentation rule, it allows to modify some parameters.

--- back


# Security Considerations

TBD

# IANA Considerations

TBD