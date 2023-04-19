---
stand_alone: true
ipr: trust200902
docname: draft-toutain-schc-access-control-00
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
  org: Nokia Bell Labs
  street:
  - 12 Rue Jean Bart
  city: 91300 Massy
  country: France
  email: ivan.martinez_bolivar@nokia.fr 
normative:
  RFC8824:
  RFC8341:
  RFC9363:
informative:
  
    
--- abstract

The framework for SCHC defines an abstract view of the rules, formalized with through a YANG Data Model. In its original description rules are static and share by 2 end-points. The use of YANG authorizes rules to be uploaded or modified in a SCHC instance and leads to some possible attacks, if the changes are not controlled. This document defines a threat model, summarizes some possible attacks and defines augmentation to the existing Data Mode in order to restrict the changes in the rule, and therefore the impact of possible attacks. 

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

When a management request arrives on a SCHC end-point, the identity of the requester must be 
checked:

 * this can be implicit, for example a LPWAN device receives it from the SCHC core instance. Authentication 
 is done at Layer 2.
 * this can be a L2 address. In a LoRaWAN network, for example the DevEUI allows the SCHC core to identify the device.
 * IP addresses may also be used as well as cryptographic keys.

The identification of the requester allows to retrieve the associated Set of Rules. These rules are enriched with access control information that will be defined in this document. If the Set of Rules does not contains any access control information, the management is not allowed to modify the Rules content.

# Threat Model

The Rule Manager (RM) is in charge of applying changes to the rules database when a management request arrives to a SCHC end pont. It is assumed that the these changes can only be effectivelly applied when it is certain that all end-points of an instance have made the change. This means that in all cases a peer of peers in an intance always share the same Set of Rules.

The selection of a rule to be applied in a certain end-point when a packet arrives is done by selecting the rule offering the smallest SCHC packet after compression.

The attack scenarios considered below are limited to the rule management layer, and only involve that a single end-point in a given instance has been compromised.

# Scenario 1: Compromised Device

A Device RM under control of an attacker sends some management messages to modify the SCHC rules in the core in order to direct the traffic to another application. The impact of this attack is different depending on the original rule:

1. Rules containing exlusively the pair MA -- CDA : [ignore -- not-send] or rules such as no-compress or no-frarmentation: 
   * There is no risk of information lost. 
   * There is a risk of DoS-type attack as it can flood empty packets that pass at the core level.
   * The attack is limited to a single end-point (the device) since it does not have the rigths to change core-level rules.

For instance ... TBD

2. Management messages aiming at changing rules where the length of the residue changes:
   * There can be a risk of desyncronising rules between the core and the compromised device.
   * The attack is limited to a single end-point (the device) since it does not have the rigths to change core-level rules.

As SCHC rules are defined for a specific traffic. An example of this can be an attacker changing en element of the rule (for instance, the dev UDP port number) and therefore no rule matches the traffic. Therefore, the core may be saturated by no-compressed messages.

# Scenario 2: Compromised Core

A Core RM under control of an attacker sends some management messages to modify the SCHC rules in the device in order to deleate devices' data. 
In such scenario, the attacker will try to inject destructive rules.

The main characteristic of these rules is that the combination of MA -- CA reduces the size of the residue, which has in turn made it more attractive since it increases the rate of compression.

The impact of this attack could be:
  * Lost of devices' information if nothing is done to preeempt a compromised core to change such a rule.


An example of this atack could be ... TBD


# YANG Access Control

YANG language allows to specify read only or read write nodes. NACM {{RFC8341}} extends this by allowing users or group of users to perform specific actions.

This granularity do not fit this the rule model. For instance, the goal is not to allow all the field-id leaves to be modified. The objective is to allow a specific rule entry to be changed and therefore some of the leaves to be modified. For instance an entry with field-id containing Uri-path may have his target-value modified, as in the same rule, the entry regarding the app-prefix should not be changed. 

The SCHC access control augments the YANG module defined in {{RFC9363}} to allow a remote entity to manipulate the rules. Several levels are defined.

  * in the set of rules, it authorizes or not a new rule to be added .
  * in a compression rule, it allows to add or remove field descriptions.
  * in a compression rule, it allows to modify some elements of the rule, such as the target-value, the matching-operator or/and the comp-decomp-action and associated values.
  * in a fragmentation rule, it allows to modify some parameters.

# YANG Data Model

The YANG DM proposed in {{AnnexA}} extends the SCHC YANG Data Model introduced in {{RFC9363}}. It adds read-only leaves containing the access rights. If these leaves are not presents, the information cannot be modified. 

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
