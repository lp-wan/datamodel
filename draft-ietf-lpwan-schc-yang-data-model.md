---
stand_alone: true
ipr: trust200902
docname: draft-ietf-lpwan-schc-yang-data-model-15
cat: std
pi:
  symrefs: 'yes'
  sortrefs: 'yes'
  strict: 'yes'
  compact: 'yes'
  toc: 'yes'

title: Data Model for Static Context Header Compression (SCHC)
abbrev: LPWAN SCHC YANG module
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
normative:
    RFC0768:
    RFC2119:
    RFC3688:
    RFC6020:
    RFC7252:
    RFC7967:
    RFC8174:
    RFC8200:
    RFC8613:
    RFC8724:
    RFC8824:
informative:
    RFC7942:
    RFC7950:
    RFC9011:
    I-D.ietf-lpwan-architecture:
    
--- abstract

This document describes a YANG data model for the SCHC (Static Context Header Compression) 
compression and fragmentation rules.


--- middle


# Introduction {#Introduction}

SCHC is a compression and fragmentation mechanism for constrained networks defined in {{RFC8724}}.
It is based on a static context shared by two entities at the boundary of the constrained network.
{{RFC8724}} provides a non formal representation of the rules used either for compression/decompression (or C/D)
or fragmentation/reassembly (or F/R). The goal of this document is to formalize the description of the rules to offer:

* the same definition on both ends, even if the internal representation is different. 
* an update of the other end to set up some specific values (e.g. IPv6 prefix, destination address,...)
* ...

{{I-D.ietf-lpwan-architecture}} illustrates the exchange of rules using the YANG data model.

This document defines a YANG module {{RFC7950}} to represent both compression and fragmentation rules, which leads to common representation for values for all the rules elements. 

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED",
"MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they
appear in all capitals, as shown here.

# SCHC rules

This document defines a YANG module to represent both compression and fragmentation rules, which leads to common representation for values for all the rules elements. 

SCHC compression is generic, the main mechanism does not refer
to a specific protocol. Any header field is abstracted through an ID, a position, a direction, and a value that can be a numerical
value or a string. {{RFC8724}} and {{RFC8824}} specify fields for IPv6 {{RFC8200}}, UDP{{RFC0768}}, CoAP {{RFC7252}} including options definied for no serveur response  {{RFC7967}} and OSCORE {{RFC8613}}. For the latter {{RFC8824}} splits this field into sub-fields.

SCHC fragmentation requires a set of common parameters that are included in a rule. These parameters are defined in {{RFC8724}}.

The YANG data model allows to select the compression or the fragmentation using the feature command.


## Compression Rules {#comp_types}

{{RFC8724}} proposes a non formal representation of the compression rule.
A compression context for a device is composed of a set of rules. Each rule contains information to
describe a specific field in the header to be compressed. 

~~~~~~

  +-----------------------------------------------------------------+
  |                      Rule N                                     |
 +-----------------------------------------------------------------+|
 |                    Rule i                                       ||
+-----------------------------------------------------------------+||
|  (FID)            Rule 1                                        |||
|+-------+--+--+--+------------+-----------------+---------------+|||
||Field 1|FL|FP|DI|Target Value|Matching Operator|Comp/Decomp Act||||
|+-------+--+--+--+------------+-----------------+---------------+|||
||Field 2|FL|FP|DI|Target Value|Matching Operator|Comp/Decomp Act||||
|+-------+--+--+--+------------+-----------------+---------------+|||
||...    |..|..|..|   ...      | ...             | ...           ||||
|+-------+--+--+--+------------+-----------------+---------------+||/
||Field N|FL|FP|DI|Target Value|Matching Operator|Comp/Decomp Act|||
|+-------+--+--+--+------------+-----------------+---------------+|/
|                                                                 |        
\-----------------------------------------------------------------/  

~~~~~~
{: #Fig-ctxt title='Compression Decompression Context'}

##Identifier generation

Identifier used in the SCHC YANG data model are from the identityref statement to ensure to be globally unique and be easily augmented if needed.  The principle to define a new type based on a group of identityref is the following:

* define a main identity ending with the keyword base-type.

* derive all the identities used in the Data Model from this base type.

* create a typedef from this base type.

The example ({{Fig-identityref}}) shows how an identityref is created for RCS (Reassembly Check Sequence) algorithms used during SCHC fragmentation. 


~~~~~
 // -- RCS algorithm types

  identity rcs-algorithm-base-type {
    description
      "Identify which algorithm is used to compute RCS.
       The algorithm also defines the size of the RCS field.";
  }

  identity rcs-RFC8724 {
    base rcs-algorithm-base-type;
    description
      "CRC 32 defined as default RCS in RFC8724. RCS is 4 byte-long";
  }

  typedef rcs-algorithm-type {
    type identityref {
      base rcs-algorithm-base-type;
    }
    description
      "type used in rules.";
  }
~~~~~
{: #Fig-identityref title='Principle to define a type based on identityref.'}


## Convention for Field Identifier

In the process of compression, the headers of the original packet are first parsed to create a list of fields. This list of fields is matched against the rules to find the appropriate rule and apply compression.  {{RFC8724}}  does not state how the field ID value is constructed. 
In examples, identification is done through a string indexed by the protocol name (e.g. IPv6.version, CoAP.version,...).

The current YANG data model includes fields definitions found in {{RFC8724}}, {{RFC8824}}.

Using the YANG data model, each field MUST be identified through a global YANG identityref.  
A YANG field ID for the protocol is always derived from the fid-base-type. Then an identity 
for each protocol is specified using the naming convention fid-\<\<protocol name>>-base-type. 
All possible fields for this protocol MUST derive from the protocol identity. The naming 
convention is "fid" followed by the protocol name and the field name. If a field has 
to be divided into sub-fields, the field identity serves as a base. 

The full field-id definition is found in {{annexA}}. A type is defined for IPv6 protocol, and each 
field is based on it. Note that the DiffServ bits derives from the Traffic Class identity.


## Convention for Field length 

Field length is either an integer giving the size of a field in bits or a specific function. {{RFC8724}} defines the
"var" function which allows variable length fields (whose length is expressed in bytes) and {{RFC8824}} defines the "tkl" function for managing the CoAP
Token length field.

The naming convention is "fl" followed by the function name.

The field length function can be defined as an identityref as described in {{annexA}}. Therefore, the type for field length is a union between an integer giving in bits the size of the length and the identityref.


## Convention for Field position

Field position is a positive integer which gives the position of a field, the default value is 1, and incremented at each repetition. 
value 0 indicates that the position is not important and is not considered during the rule selection process. 

Field position is a positive integer. The type is an uint8.

## Convention for Direction Indicator

The Direction Indicator (di) is used to tell if a field appears in both direction (Bi) or only uplink (Up) or Downlink (Dw). The naming convention is "di" followed by the Direction Indicator name.

The type is "di-type".

## Convention for Target Value {#target_value}

The Target Value is a list of binary sequences of any length, aligned to the left. In the rule, the structure will be used as a list, with index as a key. The highest index value is used to compute the size of the index sent in residue for the match-mapping CDA (Compression Decompression Action). The index allows to specify several values:

* For Equal and LSB, Target Value contains a single element. Therefore, the index is set to 0.

* For match-mapping, Target Value can contain several elements. Index values MUST start from 0 and MUST be contiguous. 

If the header field contains a text, the binary sequence uses the same enconding.

## Convention for Matching Operator

Matching Operator (MO) is a function applied between a field value provided by the parsed header and the target value. {{RFC8724}} defines 4 MO.

The naming convention is "mo" followed by the MO name.

The type is "mo-type" 


### Matching Operator arguments

They are viewed as a list, built with a tv-struct (see chapter {{target_value}}).

## Convention for Compression Decompression Actions

Compression Decompression Action (CDA) identifies the function to use for compression or decompression. 
{{RFC8724}} defines 6 CDA. 

The naming convention is "cda" followed by the CDA name.

### Compression Decompression Action arguments

Currently no CDA requires arguments, but in the future some CDA may require one or several arguments.
They are viewed as a list, of target-value type.

## Fragmentation rule {#frag_types}

Fragmentation is optional in the data model and depends on the presence of the "fragmentation" feature.  

Most of the fragmentation parameters are listed in Annex D of {{RFC8724}}. 

Since fragmentation rules work for a specific direction, they MUST contain a mandatory direction indicator.
The type is the same as the one used in compression entries, but bidirectional MUST NOT be used.

### Fragmentation mode

{{RFC8724}} defines 3 fragmentation modes:

* No Ack: this mode is unidirectionnal, no acknowledgment is sent back. 

* Ack Always: each fragmentation window must be explicitly acknowledged before going to the next.

* Ack on Error:  A window is acknowledged only when the receiver detects some missing fragments.

The type is "fragmentation-mode-type". 
The naming convention is "fragmentation-mode" followed by the fragmentation mode name.


### Fragmentation Header


A data fragment header, starting with the rule ID can be sent on the fragmentation direction. 
{{RFC8724}} indicates that the SCHC header may be composed of (cf. {{Fig-frag-header-8724}}):

* a Datagram Tag (Dtag) identifying the datagram being fragmented if the fragmentation applies concurrently on several datagrams. This field in optional and its length is defined by the rule.

* a Window (W) used in Ack-Always and Ack-on-Error modes. In Ack-Always, its size is 1. In Ack-on-Error, it depends on the rule. This field is not needed in No-Ack mode. 

* a Fragment Compressed Number (FCN) indicating the fragment/tile position within the window. This field is mandatory on all modes defined in {{RFC8724}}, its size is defined by the rule.

~~~~~

|-- SCHC Fragment Header ----|
         |-- T --|-M-|-- N --|
+-- ... -+- ... -+---+- ... -+--------...-------+~~~~~~~~~~~~~~~~~~~~
| RuleID | DTag  | W |  FCN  | Fragment Payload | padding (as needed)
+-- ... -+- ... -+---+- ... -+--------...-------+~~~~~~~~~~~~~~~~~~~~

~~~~~
{: #Fig-frag-header-8724 title='Data fragment header from RFC8724'}

### Last fragment format

The last fragment of a datagram is sent with an RCS (Reassembly Check Sequence) field to detect residual 
transmission error and possible losses in the last window. {{RFC8724}} defines a single algorithm based on Ethernet 
CRC computation. 

The naming convention is "rcs" followed by the algorithm name.

For Ack-on-Error mode, the All-1 fragment may just contain the RCS or can include a tile. The parameters defines the 
behavior:

* all-1-data-no: the last fragment contains no data, just the RCS

* all-1-data-yes: the last fragment includes a single tile and the RCS

* all-1-data-sender-choice: the last fragment may or may not contain a single tile. The receiver can detect if a tile is present.

The naming convention is "all-1-data" followed by the behavior identifier.


### Acknowledgment behavior

The acknowledgment fragment header goes in the opposite direction of data. {{RFC8724}} defines the header, composed of (see {{Fig-frag-ack}}):

* a Dtag (if present).
* a mandatory window as in the data fragment. 
* a C bit giving the status of RCS validation.  In case of failure, a bitmap follows, indicating the received tile. 


~~~~~~
|--- SCHC ACK Header ----|
         |-- T --|-M-| 1 |
+-- ... -+- ... -+---+---+~~~~~~~~~~~~~~~~~~
| RuleID |  DTag | W |C=1| padding as needed                (success)
+-- ... -+- ... -+---+---+~~~~~~~~~~~~~~~~~~

+-- ... -+- ... -+---+---+------ ... ------+~~~~~~~~~~~~~~~
| RuleID |  DTag | W |C=0|Compressed Bitmap| pad. as needed (failure)
+-- ... -+- ... -+---+---+------ ... ------+~~~~~~~~~~~~~~~

~~~~~~
{: #Fig-frag-ack title='Acknowledgment fragment header for RFC8724'}

For Ack-on-Error, SCHC defines when an acknowledgment can be sent. This can be at any time defined by the layer 2, at the end of a window (FCN all-0) 
or as a response to receiving the last fragment (FCN all-1). The naming convention is "ack-behavior" followed by the algorithm name.

### Timer values 

The state machine requires some common values to handle correctly fragmentation. 

* retransmission-timer gives the duration before sending an ack request (cf. section 8.2.2.4. of {{RFC8724}}). If specified, value must be strictly positive. 
* inactivity-timer gives  the duration before aborting a fragmentation session (cf. section 8.2.2.4. of {{RFC8724}}). The value 0 explicitly indicates that this timer is disabled.

{{RFC8724}} do not specified any range for these timers. {{RFC9011}} recommends a duration of 12 hours. In fact, the value range sould be between milliseconds for real time systems to several days. To allow a large range of applications, two parameters must be specified:

  * the duration of a tick. It is computed by this formula 2^tick-duration/10^6. When tick-duration is set to 0, the unit is the microsecond. The default value of 20 leads to a unit of 1.048575 second. A value of 32 leads to a tick duration of about 1 hour 11 minutes.
  * the number of ticks in the predefined unit. With the default tick-duration value of 20, the timers can cover a range between 1.0 sec and 19 hours covering {{RFC9011}} recommandation.

### Fragmentation Parameter 

The SCHC fragmentation protocol specifies the  the number of attempts before aborting through the parameter: 

* max-ack-requests  (cf. section 8.2.2.4. of {{RFC8724}}).


### Layer 2 parameters

The data model includes two parameters needed for fragmentation:

* l2-word-size: {{RFC8724}} base fragmentation, in bits,  on a layer 2 word which can be of any length. The default value is 8 and correspond 
to the default value for byte aligned layer 2. A value of 1 will indicate that there is no alignment and no need for padding. 
* maximum-packet-size: defines the maximum size of a uncompressed datagram. By default, the value is set to 1280 bytes.

They are defined as unsigned integer, see {{annexA}}.

# Rule definition

A rule is idenfied by a unique rule identifier (rule ID) comprising both a Rule ID value and a Rule ID length. 
The YANG grouping rule-id-type defines the structure used to represent a rule ID. A length of 0 is allowed to represent an implicit rule. 

Three types of rules are defined in {{RFC8724}}:

* Compression: a compression rule is associated with the rule ID.
* No compression: this identifies the default rule used to send a packet in extenso when no compression rule was found (see {{RFC8724}} section 6). 
* Fragmentation: fragmentation parameters are associated with the rule ID. Fragmentation is optional and feature "fragmentation" should be set. 


To access a specific rule, the rule ID length and value are used as a key. The rule is either
a compression or a fragmentation rule.  

## Compression rule

A compression rule is composed of entries describing its processing. An entry  contains all the information defined in {{Fig-ctxt}} with the types defined above. 

The compression rule described {{Fig-ctxt}} is defined by compression-content. It defines a list of
compression-rule-entry, indexed by their field id, position and direction. The compression-rule-entry 
element represent a line of the table {{Fig-ctxt}}. Their type reflects the identifier types defined in
{{comp_types}}

Some checks are performed on the values:

* target value must be present for MO different from ignore.
* when MSB MO is specified, the matching-operator-value must be present


## Fragmentation rule

A Fragmentation rule is composed of entries describing the protocol behavior. Some on them are numerical entries,
others are identifiers defined in {{frag_types}}. 




## YANG Tree


~~~~~ 
module: ietf-schc
 +-rw schc
   +-rw rule* [rule-id-value rule-id-length]
      +-rw rule-id-value                   uint32
      +-rw rule-id-length                  uint8
      +-rw (nature)?
        +-:(fragmentation) {fragmentation}?
        | +-rw fragmentation-mode        schc:fragmentation-mode-type
        | +-rw l2-word-size?             uint8
        | +-rw direction                 schc:di-type
        | +-rw dtag-size?                uint8
        | +-rw w-size?                   uint8
        | +-rw fcn-size                  uint8
        | +-rw rcs-algorithm?            rcs-algorithm-type
        | +-rw maximum-packet-size?      uint16
        | +-rw window-size?              uint16
        | +-rw max-interleaved-frames?   uint8
        | +-rw inactivity-timer
        | | +-rw ticks-duration?   uint8
        | | +-rw ticks-numbers?    uint16
        | +-rw retransmission-timer
        | | +-rw ticks-duration?   uint8
        | | +-rw ticks-numbers?    uint16
        | +-rw max-ack-requests?         uint8
        | +-rw (mode)?
        |   +-:(no-ack)
        |   +-:(ack-always)
        |   +-:(ack-on-error)
        |      +--rw tile-size?          uint8
        |      +--rw tile-in-All1?       schc:all1-data-type
        |     +--rw ack-behavior?       schc:ack-behavior-type
        +-:(compression) {compression}?
        | +-rw entry* [field-id field-position direction-indicator]
        |   +-rw field-id                    schc:fid-type
        |   +-rw field-length                schc:fl-type
        |   +-rw field-position              uint8
        |   +-rw direction-indicator         schc:di-type
        |   +-rw target-value* [index]
        |   |  +-rw value?   binary
        |   |  +-rw index    uint16
        |   +-rw matching-operator           schc:mo-type
        |   +-rw matching-operator-value* [index]
        |   |  +-rw value?   binary
        |   |  +-rw index    uint16
        |   +-rw comp-decomp-action          schc:cda-type
        |   +-rw comp-decomp-action-value* [index]
        |      +-rw value?   binary
        |      +-rw index    uint16
        +-:(no-compression)
~~~~~ 
{: #Fig-model-overview title='Overview of SCHC data model}

# YANG Module {#annexA}


~~~~
<CODE BEGINS> file "ietf-schc@2022-07-11.yang"
{::include ietf-schc@2022-07-11.yang}
<CODE ENDS>
~~~~
{: #Fig-schc title="SCHC data model}

# Implementation Status

<!--NOTE TO RFC EDITOR:  remove the entire section before
   publication, as well as the reference to RFC 7942. -->


This section records the status of known implementations of the
protocol defined by this specification at the time of posting of
this Internet-Draft, and is based on a proposal described in
{{RFC7942}}.  The description of implementations in this section is
intended to assist the IETF in its decision processes in
progressing drafts to RFCs.  Please note that the listing of any
individual implementation here does not imply endorsement by the
IETF.  Furthermore, no effort has been spent to verify the
information presented here that was supplied by IETF contributors.
This is not intended as, and must not be construed to be, a
catalog of available implementations or their features.  Readers
are advised to note that other implementations may exist.

According to {{RFC7942}}, "this will allow reviewers and working
groups to assign due consideration to documents that have the
benefit of running code, which may serve as evidence of valuable
experimentation and feedback that have made the implemented
protocols more mature.  It is up to the individual working groups
to use this information as they see fit".

* Openschc is implementing the conversion between the local rule 
  representation and the representation conform to the data model 
  in JSON and CBOR (following -08 draft).


# IANA Considerations

This document registers one URIs and one YANG modules.

##  URI Registration

This document requests IANA to register the following four URIs in the "IETF XML Registry" {{RFC3688}}:

> URI:  urn:ietf:params:xml:ns:yang:ietf-schc

> Registrant Contact:  The IESG.

> XML:  N/A; the requested URI is an XML namespace.


##  YANG Module Name Registration

This document registers the following one YANG modules in the "YANG Module Names" registry {{RFC6020}}.

> name:           ietf-schc 

> namespace:      urn:ietf:params:xml:ns:yang:ietf-schc

> prefix:         schc

> reference:      RFC XXXX Data Model for Static Context Header Compression (SCHC)

# Security Considerations

The YANG module specified in this document defines a schema for data that is designed to be accessed via network management protocols such as NETCONF {{!RFC6241}} or RESTCONF {{!RFC8040}}. The lowest NETCONF layer is the secure transport layer, and the mandatory-to-implement secure transport is Secure Shell (SSH) {{!RFC6242}}. The lowest RESTCONF layer is HTTPS, and the mandatory-to-implement secure transport is TLS 
{{!RFC8446}}.

The Network Configuration Access Control Model (NACM) {{!RFC8341}} provides the means to restrict access for particular NETCONF or RESTCONF users to a preconfigured subset of all available NETCONF or RESTCONF protocol operations and content.

This data model formalizes the rules elements described in {{RFC8724}} for compression and fragmentation. As explained in the architecture document {{I-D.ietf-lpwan-architecture}}, a rule can be read, created, updated or deleted in response to a management request. These actions can be done between two instances of SCHC or between a SCHC instance and a rule repository.

~~~~~
                     create
          (-------)  read   +=======+ *
          ( rules )<------->|Rule   |<--|-------->
          (-------)  update |Manager|   NETCONF, RESTCONF or CORECONF
             . read  delete +=======+   request
             .
          +-------+
      <===| R & D |<===
      ===>| C & F |===>
          +-------+
~~~~~

The rule contains some sensible informations such as the application IPv6 address. An attacker by changing a rule content may block the communication or intercept the traffic. Therefore, the identity of the requester must be validated. This can be done through certificates or access lists.

The full tree is sensitive, since it represents all the elements that can be managed.  This module aims to be encapsulated into a YANG module including access right and identities. 



# Acknowledgements

The authors would like to thank Dominique Barthel, Carsten Bormann, Ivan Martinez, Alexander Pelov for their careful reading and valuable inputs. A special thanks for 
Carl Moberg, Tom Petch
and Eric Vyncke for their explanations and wise advices when building the model.




--- back
