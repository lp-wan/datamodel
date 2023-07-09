---
stand_alone: true
ipr: trust200902
docname: draft-toutain-schc-access-control-01
area: Internet
kw: Internet-Draft
cat: std
pi:
  symrefs: 'yes'
  sortrefs: 'yes'
  strict: 'yes'
  compact: 'yes'
  toc: 'yes'

title: SCHC Rule Access Control
abbrev: SCHC AC
wg: SCHC Working Group
author:
- ins: A. Minaburo
  name: Ana Minaburo
  org: Consultant
  street: Rue de Rennes
  city: 35510 Cesson-Sevigne Cedex
  country: France
  email: anaminaburo@gmail.com
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
  email: ivan.martinez_bolivar@nokia-bell-labs.com 
normative:
  RFC2119:
  RFC6241:
  RFC8040:
  RFC8174:
  RFC8724:
  RFC8824:
  RFC9363:
  RFC8341:  
  I-D.ietf-core-comi:
  I-D.ietf-schc-architecture:
informative:
  
    
--- abstract

The framework for SCHC defines an abstract view of the rules, formalized through a YANG Data Model. In its original description, rules are static and shared by two endpoints. The use of YANG authorizes rules to be uploaded or modified in a SCHC instance and leads to some possible attacks if the changes are not controlled. This document defines a threat model, summarizes some possible attacks, and defines augmentation to the existing Data Model in order to restrict the changes in the rule and, therefore, the impact of possible attacks. 

--- middle

# Introduction

SCHC is a compression and fragmentation mechanism defined in {{RFC8724}} while {{RFC9363}} provides a YANG Data Model for formal representation of SCHC Rules used either for compression/decompression (C/D) or fragmentation/reassembly (F/R). [LPWAN-ARCH] illustrates the use of several protocols for rule management using the YANG Data Model, such as CORECONF {{I-D.ietf-core-comi}}, NETCONF{{RFC6241}}, RESTCONF {{RFC8040}}. The inappropriate use of any of these protocols leads to some possible attacks. The goal of this document is to define a threat model, summarize some possible attacks, and define augmentation to the existing Data Model in order to restrict the changes in the rules and, therefore, the impact of possible attacks. 

# Conventions and Definitions

{::boilerplate bcp14-tagged}


# Terminology

ToDo
* Access Control. 
* Management request processing: The NETCONF, RESTCONF or CORECONF request is processed and passed to the end-point Rule Manager.
* Rule Manager (RM). 
* Context. SCHC Rules

  
# SCHC Management Architecture

Figure {{Fig-archi-overview}} presents the management part of the SCHC architecture.

~~~~~~
  .....................................
  .  ........................         .
  v  ^    create             v         ^   
(-------)  read  +====+    +==+==+   +===+===+   +=========+
(Context)<------>| RM |<-->|Mgmt.|<==|Access |<==|Other end|<=== 
(-------) update +====+    |req. |   |Control|   |auth.    | Management
          delete           |proc.|   +=======+   +=========+ Request
                           +=====+                           NETCONF,
                                                             RESTCONF
                                                          or CORECONF
~~~~~~
{: #Fig-archi-overview title='Overview of management architecture.'}


When a management request arrives on a SCHC endpoint, several processes should be passed before effectively creating or updating a Rule:

1. Other end authentication: the identity of the requester must be verified:
   * This can be implicit, for example, an LPWAN device that receives it from the SCHC core. Hence, authentication is done at Layer 2.
   * This can be an L2 address. In a LoRaWAN network, for example, the DevEUI allows the SCHC core to identify the device.
   * IP addresses may also be used, as well as cryptographic keys.
2. Access control: Once authenticated, the associated Set of Rules of the instance is retrieved. 
   * These rules are enriched with access control information that will be defined in this document. 
   * If the Set of Rules does not contain any access control information, the end-point is not allowed to modify the Rules' content.
3. Management request processing: The NETCONF, RESTCONF or CORECONF request is processed and passed to the end-point Rule Manager.
5. The Rule Manager (RM) applies the changes (create, read, update, or delete) to the Rule database. 

# Threat Model

The RM is in charge of applying changes to the rules database when a management request arrives at a SCHC end-point. It is assumed that these changes can only be effectively applied when it is sure that all end-points of an instance have made the change. This means that in all cases, a peer of peers in an instance always shares the same Set of Rules.

The selection of a rule to be applied in an accurate endpoint when a packet arrives is made by selecting the rule offering the best-performance SCHC packet after compression.

The attack scenarios considered below are limited to the rule management layer and only involve that a single endpoint in a given instance has been compromised.
This means that the authentication is bypassed. Therefore, the compromised endpoint is able to effectively deliver management requests using NETCONF, RESTCONF, or CORECONF to the other endpoint.

# SCHC TV/MO/CDA possible combinations
SCHC compression behavior uses the TV, MO, and CDA to generate the correct residue. But not all the combinations of this fields descriptors are possible, and then an attack can be detected or avoided. {{Fig-combinations}} shows all the combinations and those that are enabled. SCHC defines two TV values: set and not set. SCHC MO can be Equal, Ignore, MSB, or Match-mapping. And SCHC CDA can be not-sent, value-sent, mapping-sent, LSB, compute-*, DevIID, or AppIID.

~~~~~~

    +-----------------+------------------------------------------------------+
    |                 |                      CDA                             |
    |  TV   /  MO     +--------+---------------+-----+---------+------+------+
    |                 |not-sent| value |mapping| LSB |compute-*|DevIID|AppIID|
    |                 |        | -sent | -sent |     |         |      |      |  
    +-----------------+--------+-------+-------+-----+---------+------+------+
    |  set  /  Equal  |  ok    |absurd |   x   |  x  | absurd  |absurd|absurd|
    +-----------------+--------+-------+-------+-----+---------+------+------+
    | not set / Equal |   x    |   x   |   x   |  x  | absurd  |absurd|absurd|
    +-----------------+--------+-------+-------+-----+---------+------+------+
    |  set  / Ignore  | ok (D) | absurd|    x  |  x  |   ok    |  ok  |  ok  |
    +-----------------+--------+-------+-------+-----+---------+------+------+
    |not set / Ignore |   x    |  ok   |    x  |  x  |   ok    |  ok  |  ok  |
    +-----------------+--------+-------+-------+-----+---------+------+------+
    |  set   /   MSB  | absurd |absurd |    x  |  ok |  absurd |absurd|absurd|
    +-----------------+--------+-------+-------+-----+---------+------+------+
    | not set /  MSB  | absurd | absurd|    x  | ok  |  absurd |absurd|absurd|
    +-----------------+--------+-------+-------+-----+---------+------+------+
    |  set   /  Match |   x    | absurd|   ok  |  x  |  absurd |absurd|absurd|
    |         -mapping|        |       |       |     |         |      |      |
    +-----------------+--------+-------+-------+-----+---------+------+------+
    |not set /  Match |   x    |   x   | absurd|  x  |  absurd |absurd|absurd|
    |         -mapping|        |       |       |     |         |      |      |
    +-----------------+--------+-------+-------+-----+---------+------+------+


~~~~~~
{: #Fig-combinations title='SCHC TV, MO, CDA valid combinations'}


# Attack Scenarios
## Scenario 1: Compromised Device

A Device RM, under the control of an attacker, sends some management messages to modify the SCHC rules in the core in order to direct the traffic to another application. The impact of this attack is different depending on the original rule:

1. Rules containing exclusively the pair MO -- CDA : [ignore -- not-sent] or rules such as no-compress or no-fragmentation: 
   * There is no risk of information lost. 
   * There is a risk of a DoS-type attack as it can flood empty packets that pass at the core level.

For example ... TBD

The attack is limited to a single end-point (the device) since it does not have the right to change core-level rules.

2. Management messages aiming at changing rules where the length of the residue changes:
   * There can be a risk of desynchronizing rules between the core and the compromised device.
   * The attack is limited to a single end-point (the device) since it does not have the right to change core-level rules.

As SCHC rules are defined for specific traffic. An example of this can be an attacker changing an element of the rule (the dev UDP port number, for instance), and therefore no rule matches the traffic. Therefore, the core may be saturated by no-compressed messages.

## Scenario 2: Compromised Core

A Core RM, under the control of an attacker, sends some management messages to modify the SCHC rules in the device in order to delete the device's data. 
In such a scenario, the attacker will try to inject destructive rules.

The main characteristic of these rules is that the combination of MA -- CA reduces the size of the residue, which has, in turn, made it more attractive since it increases the rate of compression.

The impact of this attack could be:
  * Lost of devices' information if nothing is done to preempt a compromised core to change such a rule.

An example of this attack could be ... TBD

# YANG Access Control

YANG language allows to specify read-only or read write nodes. NACM {{RFC8341}} extends this by allowing users or groups of users to perform specific actions.

This granularity does not fit this rule model. For instance, the goal is not to allow all the field-id leaves to be modified. The objective is to allow a specific rule entry to be changed and, therefore, some of the leaves to be modified. For instance, an entry with FID containing Uri-path may have its target value modified, as in the same rule, the entry regarding the application prefix should not be changed. 

The SCHC access control augments the YANG module defined in {{RFC9363}} to allow a remote entity to manipulate the rules. Several levels are defined.

  * in the set of rules, it authorizes or not a new rule to be added.
  * in a compression rule, it allows adding or removing field descriptions.
  * in a compression rule, it allows modifying some elements of the rule, such as the TV, MO, or/and CDA, and associated values.
  * in a fragmentation rule, it allows modifying some parameters.

# YANG Data Model

The YANG DM proposed in {{AnnexA}} extends the SCHC YANG Data Model introduced in {{RFC9363}}. It adds read-only leaves containing access rights. If these leaves are not present, the information cannot be modified. 

## leaf ac-modify-set-of-rules

This leaf controls modifications applied to a set of rules. They are specified with the rule-access-right enumeration:

* no-change (0): rules cannot be modified in the Set of Rules. This is the equivalent of having no access control elements in the set of rules. 

* modify-existing-element (1): an existing rule may be modified.

* add-remove-element (2): a rule can be added or deleted from the Set of Rules, or an existing rule can be modified.

## leaf ac-modify-compression-rule

This leaf allows to modify a compression element. To be active, leaf ac-modify-set-of-rules MUST be set to modify-existing-element or add-remove-element. This leaf uses the same enumeration as add-remove-element:

* no-change (0): The rule cannot be modified. 

* modify-existing-element (1): an existing Field Description may be modified.

* add-remove-element (2): a Field Description can be added or deleted from the Rule or an existing rule can be modified.

## leaf ac-modify-field

This leaf allows to modify a Field Description in a compression rule. To be active, leaves ac-modify-set-of-rules and ac-modify-compression-rule MUST be set to modify-existing-element  or add-remove-element and ac-modify-compression-rule and leaf 



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
