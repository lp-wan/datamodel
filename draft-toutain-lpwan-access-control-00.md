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

Figure {{Fig-archi-overview}} focuses on the management part of the SCHC architecture. 

~~~~~~
     .......................................................
     .   .................................                 .
     v   ^                               v                 ^   
   (--------)     +----------+        +-------+    +-------+-------+
   ( Set of )<--->|coreconf  |<=======|Access |<===| other end     |<=== 
   ( Rules  )     |request   |        |Control|    | authentication|
   (--------)     |processing|        +-------+    +---------------+
                  +----------+
~~~~~~
{: #Fig-archi-overview title='Overview of management architecture.'}

When a management request arrives on a SCHC instance, the identity of the requester must be 
checked:

 * this can be implicit, for instance a LPWAN device receives it from the  SCHC core instance. Authentication 
 is done at Layer 2.
 * this can be a L2 address. In a LoRaWAN network, the DevEUI allows the SCHC core instance to identify the device.
 * IP addresses may also be used as well as cryptographic keys.

 The identification of the requester allows to retrieve the associated Set of Rules. This rules are enriched with
 access control information that will be defined in this document. If the Set of Rules do not contains any access control information, the management is not allowed to modify the Rules content.

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

# YANG Data Model

The YANG DM proposed in {{AnnexA}} extends the SCHC YANG Data Model introduced in {{I-D.ietf-lpwan-schc-yang-data-model}}. It adds read-only leaves containing the access rights. If these leaves are not presents, the information cannot be modified. 

## leaf ac-modify-set-of-rules

This leaf controls modifications applied to a set of rules. They are specified with the rule-access-right enumeration:

* no-change (0): rules cannot be modified in the Set of Rules. This is the equivalent of having no access control elements in the set of rules. 

* modify-existing-element (1): an existing rule may be modified.

* add-remove-element (2): a rule can be added or deleted from the Set of Rules or an existing rule can be modified.

## leaf ac-modify-compression-rule

This leaf allows to modify a compression element. To be active, leaf ac-modify-set-of-rules MUST be set to modify-existing-element  or add-remove-element. This leaf uses the same enumeration as add-remove-element:

* no-change (0): The rule cannot be modified. 

* modify-existing-element (1): an existing Field Description may be modified.

* add-remove-element (2): a Field Description can be added or deleted from the Rule or an existing rule can be modified.

## leaf ac-modify-field

This leaf allows to modify a Field Description in a compression rule. To be active, leaves ac-modify-set-of-rules and ac-modify-compression-rule MUST be set to modify-existing-element  or add-remove-element and ac-modifiy-compression-rule and leaf 



--- back

# YANG Data Model {#AnnexA}

~~~~
<CODE BEGINS> file "ietf-schc-access-control@2023-02-14.yang"
{::include ietf-schc-access-control@2023-02-14.yang}
<CODE ENDS>
~~~~

# Security Considerations

TBD

# IANA Considerations

TBD