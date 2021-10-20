---
stand_alone: true
ipr: trust200902
docname: draft-ietf-lpwan-schc-yang-data-model-06
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
    RFC8724:
    RFC8824:
    I-D.barthel-lpwan-oam-schc:
    RFC7252:
    I-D.ietf-lpwan-schc-compound-ack:

    
--- abstract

This document describes a YANG data model for the SCHC (Static Context Header Compression) 
compression and fragmentation rules.

--- middle

# Introduction {#Introduction}

# SCHC rules

SCHC is a compression and fragmentation mechanism for constrained networks defined in {{RFC8724}}.
It is based on a static context shared by two entities at the boundary of the constrained network.
{{RFC8724}} provides a non formal representation of the rules used either for compression/decompression (or C/D)
or fragmentation/reassembly (or F/R). The goal of this document is to formalize the description of the rules to offer:

* the same definition on both ends, even if the internal representation is different. 
* an update of the other end to set up some specific values (e.g. IPv6 prefix, Destination address,...)
* ...

This document defines a YANG module to represent both compression and fragmentation rules, which leads to common representation for values for all the rules elements. 

SCHC compression is generic, the main mechanism does not refer
to a specific protocol. Any header field is abstracted through an ID, a position, a direction, and a value that can be a numerical
value or a string. {{RFC8724}} and {{RFC8824}} specify fields for IPv6, UDP, CoAP and OSCORE. {{I-D.barthel-lpwan-oam-schc}} describes 
ICMPv6 header compression and {{I-D.ietf-lpwan-schc-compound-ack}} includes a new fragmentation behavior.

SCHC fragmentation requires a set of common parameters that are included in a rule. These parameters are defined in {{RFC8724}}.


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

Identifier used in the SCHC YANG Data Model are from the identityref statement to ensure to be globally unique and be easily augmented if needed.  The principle to define a new type based on a group of identityref is the following:

* define a main identity ending with the keyword base-type.

* derive all the identity used in the Data Model from this base type.

* create a typedef from this base type.

The example ({{Fig-identityref}}) shows how an identityref is created for RCS algorithms used during SCHC fragmentation. 


~~~~~

  // -- RCS algorithm types

  identity rcs-algorithm-base-type {
    description
      "identify which algorithm is used to compute RSC.
       The algorithm also defines the size if the RSC field.";
  }

  identity rcs-RFC8724 {
    base rcs-algorithm-base-type;
    description
      "CRC 32 defined as default RCS in RFC8724.";
  }

  typedef rcs-algorithm-type {
    type identityref {
      base rcs-algorithm-base-type;
    }
    description
      "type used in rules";
  }
~~~~~
{: #Fig-identityref title='Principle to define a type based on identityref.'}


##Field Identifier

In the process of compression, the headers of the original packet are first parsed to create a list of fields. This list of fields is matched against the rules to find the appropriate rule and apply compression.  {{RFC8724}}  do not state how the field ID value can be constructed. 
In examples, identification is done through a string indexed by the protocol name (e.g. IPv6.version, CoAP.version,...).

The current YANG Data Model includes fields definitions found in {{RFC8724}}, {{RFC8824}}, and {{I-D.barthel-lpwan-oam-schc}}.

Using the YANG model, each field MUST be identified through a global YANG identityref.  
A YANG field ID for the protocol always derives from the fid-base-type. Then an identity 
for each protocol is specified using the naming convention fid-<<protocol name>>-base-type. 
All possible fields for this protocol MUST derive from the protocol identity. The naming 
convention is "fid" followed by the protocol name and the field name. If a field has 
to be divided into sub-fields, the field identity serves as a base. 

The full field-id definition is found in {{annexA}}. The example {{Fig-ex-field-id}} 
gives the first field ID definitions. A type is defined for IPv6 protocol, and each 
field is based on it. Note that the DiffServ bits derives from the Traffic Class identity.

~~~~~

  identity fid-base-type {
    description
      "Field ID base type for all fields";
  }

  identity fid-ipv6-base-type {
    base fid-base-type;
    description
      "Field IP base type for IPv6 headers described in RFC 8200";
  }

  identity fid-ipv6-version {
    base fid-ipv6-base-type;
    description
      "IPv6 version field from RFC8200";
  }

  identity fid-ipv6-trafficclass {
    base fid-ipv6-base-type;
    description
      "IPv6 Traffic Class field from RFC8200";
  }

  identity fid-ipv6-trafficclass-ds {
    base fid-ipv6-trafficclass;
    description
      "IPv6 Traffic Class field from RFC8200,
       DiffServ field from RFC3168";
  }
  
  ...

~~~~~
{: #Fig-ex-field-id title='Definition of identityref for field IDs'}


The type associated to this identity is fid-type (cf. {{Fig-field-id-type}})

~~~~~
  typedef fid-type {
    type identityref {
      base fid-base-type;
    }
    description
      "Field ID generic type.";
  }
~~~~~
{: #Fig-field-id-type title='Type definition for field IDs'}


## Field length 

Field length is either an integer giving the size of a field in bits or a specific function. {{RFC8724}} defines the
"var" function which allows variable length fields in byte and {{RFC8824}} defines the "tkl" function for managing the CoAP
Token length field.

The naming convention is "fl" followed by the function name.

~~~~~
  identity fl-base-type {
    description
      "Used to extend field length functions";
  }

  identity fl-variable {
    base fl-base-type;
    description
      "Residue length in Byte is sent as defined in 
      for CoAP in RFC 8824 (cf. 5.3)";
  }

  identity fl-token-length {
    base fl-base-type;
    description
      "Residue length in Byte is sent as defined in 
      for CoAP in RFC 8824 (cf. 4.5)";
  }
~~~~~
{: #Fig-ex-field-length title='Definition of identityref for Field Length'}

Field ID, field length function can be defined as an identityref as shown in {{Fig-ex-field-length}}.

Therefore, the type for field length is a union between an integer giving in bits the size of the length and the identityref (cf. {{Fig-ex-field-length-union}}).

~~~~~
  typedef fl-type {
    type union {
      type int64; /* positive length in bits */
      type identityref { /* function */
        base fl-base-type;
      }
    }
    description
      "Field length either a positive integer giving the size in bits
       or a function defined through an identityref.";
  }
~~~~~
{: #Fig-ex-field-length-union title='Type definition for field Length'}


## Field position

Field position is a positive integer which gives the position of a field, the default value is 1, and incremented at each repetition. 
value 0 indicates that the position is not important and is not considered during the rule selection process. 

Field position is a positive integer. The type is an uint8.

## Direction Indicator

The Direction Indicator (di) is used to tell if a field appears in both direction (Bi) or only uplink (Up) or Downlink (Dw). 

~~~~~
 
  identity di-base-type {
    description
      "Used to extend direction indicators";
  }

  identity di-bidirectional {
    base di-base-type;
    description
      "Direction Indication of bi directionality in 
      RFC 8724 (cf. 7.1)";
  }

  identity di-up {
    base di-base-type;
    description
      "Direction Indication of upstream defined in 
      RFC 8724 (cf. 7.1)";
  }

  identity di-down {
    base di-base-type;
    description
      "Direction Indication of downstream defined in 
      RFC 8724 (cf. 7.1)";
  }

~~~~~
{: #Fig-ex-field-DI title='Definition of identityref for direction indicators'}

{{Fig-ex-field-DI}} gives the identityref for Direction Indicators. The naming convention is "di" followed by the Direction Indicator name.

The type is "di-type" (cf. {{Fig-field-DI-type}}).

~~~~~
  typedef di-type {
    type identityref {
      base di-base-type;
    }
    description
      "Direction in LPWAN network, up when emitted by the device,
       down when received by the device, bi when emitted or received by the device.";
  }

~~~~~
{: #Fig-field-DI-type title='Type definition for direction indicators'}

## Target Value

The Target Value is a list of binary sequences of any length, aligned on the left. {{Fig-ex-TV}} gives the definition of a single element of a Target Value. In the rule, this will be used as a list, with position as a key. The highest position value is used to compute the size of the index sent in residue for LSB CDA. The position allows to specify several values:

* For Equal and LSB, a single value is used, such as for the equal or LSB CDA, the position is set to 0.

* For match-mapping, several of these values can be contained in a Target Value field.  Position values must start from 0 and be contiguous. 


~~~~~
  grouping tv-struct {
    description
      "Define the target value element. Always a binary type, strings
       must be converted to binary. field-id allows the conversion to the appropriate
       type.";
    leaf value {
      type binary;
    }
    leaf position {
      type uint16;
      description
        "If only one element position is 0, otherwise position is the
         the position in the matching list.";
    }
  }
~~~~~
{: #Fig-ex-TV title='Definition of target value'}


## Matching Operator

Matching Operator (MO) is a function applied between a field value provided by the parsed header and the target value. {{RFC8724}} defines 4 MO as listed in {{Fig-ex-MO}}.

~~~~~
  identity mo-base-type {
    description
      "Used to extend Matching Operators with SID values";
  }

  identity mo-equal {
    base mo-base-type;
    description
      "Equal MO as defined RFC 8724 (cf. 7.3)";
  }

  identity mo-ignore {
    base mo-base-type;
    description
      "Ignore MO as defined RFC 8724 (cf. 7.3)";
  }

  identity mo-msb {
    base mo-base-type;
    description
      "MSB MO as defined RFC 8724 (cf. 7.3)";
  }

  identity mo-match-mapping {
    base mo-base-type;
    description
      "match-mapping MO as defined RFC 8724 (cf. 7.3)";
  }

~~~~~
{: #Fig-ex-MO title='Definition of identityref for Matching Operator '}

The naming convention is "mo" followed by the MO name.

The type is "mo-type" (cf. {{Fig-MO-type}})

~~~~~
  typedef mo-type {
    type identityref {
      base mo-base-type;
    }
    description
      "Matching Operator (MO) to compare fields values with target values";
  }
~~~~~
{: #Fig-MO-type title='Type definition for Matching Operator'}

### Matching Operator arguments


They are viewed as a list of tv-struct.

## Compression Decompression Actions

Compression Decompression Action (CDA) identified the function to use either for compression or decompression. 
{{RFC8724}} defines 6 CDA. 

{{Fig-CDA-type}} gives some CDA definition, the full definition is in {{annexA}}.

~~~~~
  identity cda-base-type {
    description
      "Compression Decompression Actions";
  }

  identity cda-not-sent {
    base cda-base-type;
    description
      "not-sent CDA as defines in RFC 8724 (cf. 7.4)";
  }

  identity cda-value-sent {
    base cda-base-type;
    description
      "value-sent CDA as defines in RFC 8724 (cf. 7.4)";
  }

  identity cda-lsb {
    base cda-base-type;
    description
      "LSB CDA as defines in RFC 8724 (cf. 7.4)";
  }

  identity cda-mapping-sent {
    base cda-base-type;
    description
      "mapping-sent CDA as defines in RFC 8724 (cf. 7.4)";
  }

    ....
~~~~~
{: #Fig-ex-CDA title='Definition of identityref for  Compresion Decompression Action'}

The naming convention is "cda" followed by the CDA name.


~~~~~
  typedef cda-type {
    type identityref {
      base cda-base-type;
    }
    description
      "Compression Decompression Action to compression or decompress a field.";
  }

~~~~~
{: #Fig-CDA-type title='Type definition for Compresion Decompression Action'}

### Compression Decompression Action arguments

Currently no CDA requires arguments, but the future some CDA may require several arguments.
They are viewed as a list of target-values-type.

## Fragmentation rule {#frag_types}

Fragmentation is optional in the data model and depends on the presence of the "fragmentation" feature.  

Most of parameters for fragmentation are defined in Annex D of {{RFC8724}}. 

Since fragmentation rules work for a specific direction, they contain a mandatory direction.
The type is the same as the one used in compression entries, but the use of bidirectional is 
forbidden. 

### Fragmentation mode

{{RFC8724}} defines 3 fragmentation modes:

* No Ack: this mode is unidirectionnal, no acknowledgment is sent back. 

* Ack Always: each fragmentation window must be explicitly acknowledged before going to the next.

* Ack on Error:  A window is acknowledged only when the receiver detects some missing fragments.

{{Fig-frag-mode}} give the definition for identifiers from these three modes.

~~~~
identity fragmentation-mode-base-type {
    description
      "Fragmentation mode";
  }

  identity fragmentation-mode-no-ack {
    base fragmentation-mode-base-type;
    description
      "No Ack of RFC 8724.";
  }

  identity fragmentation-mode-ack-always {
    base fragmentation-mode-base-type;
    description
      "Ack Always of RFC8724.";
  }

  identity fragmentation-mode-ack-on-error {
    base fragmentation-mode-base-type;
    description
      "Ack on Error of RFC8724.";
  }

  typedef fragmentation-mode-type {
    type identityref {
      base fragmentation-mode-base-type;
    }
    description
      "type used in rules";
  }
~~~~
{: #Fig-frag-mode title='Definition of fragmentation mode identifer'}

The naming convention is "fragmentation-mode" followed by the fragmentation mode name.


### Fragmentation Header


A data fragment header, directly following the rule ID can be sent on the fragmentation direction. 
The direction is mandatory and must be up or down. bidirectional is forbidden. The SCHC header may be composed of (cf. {{Fig-frag-header-8724}}):

* a Datagram Tag (Dtag) identifying the datagram being fragmented if the fragmentation applies concurrently on several datagrams. This field in optional and its length is defined by the rule.

* a Window (W) used in Ack-Always and Ack-on-Error modes. In Ack-Always, its size is 1 and depends on the rule in Ack-on-Error. This field is not need in No-Ack mode. 

* a Fragment Compressed Number (FCN) indicating the fragment/tile position on the window. This field is mandatory on all modes defined in {{RFC8724}}, its size is defined by the rule.

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
CRC computation. The identity of the RCS algorithm is shown in {{Fig-frag-RCS}}.

~~~~~~
  // -- RCS algorithm types

  identity rcs-algorithm-base-type {
    description
      "Identify which algorithm is used to compute RSC.
       The algorithm defines also the size if the RSC field.";
  }

  identity rcs-RFC8724 {
    base rcs-algorithm-base-type;
    description
      "CRC 32 defined as default RCS in RFC8724.";
  }

  typedef rcs-algorithm-type {
    type identityref {
      base rcs-algorithm-base-type;
    }
    description
      "type used in rules";
  }
~~~~~~~
{: #Fig-frag-RCS title='type definition for RCS'}

The naming convention is "rcs" followed by the algorithm name.

For Ack-on-Error mode, the All-1 fragment may just contain the RCS or can include a tile. The parameters defined in {{Fig-frag-all1-data}} allows to define the 
behavior:

* all1-data-no: the last fragment contains no data, just the RCS

* all1-data-yes: the last fragment includes a single tile and the RCS

* all1-data-sender-choice: the last fragment may or may not contain a single tile. The receiver can detect if a tile is present.

~~~~
 // -- All1 with data types

  identity all1-data-base-type {
    description
      "Type to define when to send an Acknowledgment message";
  }

  identity all1-data-no {
    base all1-data-base-type;
    description
      "All1 contains no tiles.";
  }

  identity all1-data-yes {
    base all1-data-base-type;
    description
      "All1 MUST contain a tile";
  }

  identity all1-data-sender-choice {
    base all1-data-base-type;
    description
      "Fragmentation process choose to send tiles or not in all1.";
  }

  typedef all1-data-type {
    type identityref {
      base all1-data-base-type;
    }
    description
      "Type used in rules";
  }

~~~~
{: #Fig-frag-all1-data title='type definition for RCS'}

The naming convention is "all1-data" followed by the behavior identifier.


### Acknowledgment behavior

A cknowledgment fragment header goes in the opposite direction of data. The header is composed of (see {{Fig-frag-ack}}):

* a Dtag (if present).
* a mandatory window as in the data fragment. 
* a C bit giving the status of RCS validation.  In case of failure, a bitmap follows, indicating received fragment/tile. The size of the bitmap is given by the FCN value.

NOTE: IN THE DATA MODEL THERE IS A max-window-size FIELD TO LIMIT THE BITMAP SIZE, BUT IS NO MORE IN RFC8724! DO WE KEEP IT?

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

For Ack-on-Error, SCHC defined  when acknowledgment can be sent. This can be at any time defined by the layer 2, at the end of a window (FCN All-0) 
or at the end of the fragment (FCN All-1). The following identifiers (cf. {{Fig-frag-ack-behavior}}) define the acknowledgment behavior.

~~~~~

// -- Ack behavior 

  identity ack-behavior-base-type {
    description
      "Define when to send an Acknowledgment message";
  }

  identity ack-behavior-after-All0 {
    base ack-behavior-base-type;
    description
      "Fragmentation expects Ack after sending All0 fragment.";
  }

  identity ack-behavior-after-All1 {
    base ack-behavior-base-type;
    description
      "Fragmentation expects Ack after sending All1 fragment.";
  }

  identity ack-behavior-always {
    base ack-behavior-base-type;
    description
      "Fragmentation expects Ack after sending every fragment.";
  }

  typedef ack-behavior-type {
    type identityref {
      base ack-behavior-base-type;
    }
    description
      "Type used in rules";
  }

~~~~~
{: #Fig-frag-ack-behavior title='bitmap generation behavior'}

The naming convention is "ack-behavior" followed by the algorithm name.


For Ack-onError, {{RFC8724}} allows a single bitmap in an acknowledment fragment, and {{I-D.ietf-lpwan-schc-compound-ack}} proposes to acknowledge several windows on a single ack fragment.
The following identifiers (cf. {{Fig-frag-bitmap}}) define the behavior.

~~~~~~
  identity bitmap-format-base-type {
    description
      "Define how the bitmap is defined in ACK messages.";
  }

  identity bitmap-RFC8724 {
    base bitmap-format-base-type;
    description
      "Bitmap as defined in RFC8724.";
  }

  identity bitmap-compound-ack {
    base bitmap-format-base-type;
    description
      "Compound Ack.";
  }

  typedef bitmap-format-type {
    type identityref {
      base bitmap-format-base-type;
    }
    description
      "type used in rules";
  }

~~~~~~
{: #Fig-frag-bitmap title='bitmap generation behavior'}

The naming convention is "bitmap" followed by the algorithm name.


### Fragmentation Parameters



The state machine requires some common values to handle fragmentation:

* retransmission-timer gives in seconds the duration before sending an ack request (cf. section 8.2.2.4. of {{RFC8724}}). If specified, value must be higher or equal to 1. 
* inactivity-timer gives in seconds the duration before aborting (cf. section 8.2.2.4. of {{RFC8724}}), value of 0 explicitly indicates that this timer is disabled.
* max-ack-requests gives the number of attempts before aborting (cf. section 8.2.2.4. of {{RFC8724}}).
* maximum-packet-size gives in bytes the larger packet size that can be reassembled. 

The are defined as unsigned integer, see {{annexA}}.

### Layer 2 parameters

The data model includes two parameters needed for fragmentation:

* l2-word-size: {{RFC8724}} base fragmentation on a layer 2 word which can be of any length. The default value is 8 and correspond 
to the default value for byte aligned layer 2. A value of 1 will indicate that there is no alignment and no need for padding. 
* maximum-packet-size: defines the maximum size of a uncompressed datagram. By default, the value is set to 1280 bytes.

They are defined as unsigned integer, see {{annexA}}.




# Rule definition

A rule is either a C/D or an F/R rule. A rule is identified by the rule ID value and its associated length. 
The YANG grouping rule-id-type defines the structure used to represent a rule ID. Length of 0 is allowed to represent an implicit rule. 

Three types of rules are defined in {{RFC8724}}:

* Compression: a compression rule is associated to the rule ID.
* No compression: nothing is associated to the rule ID.
* Fragmentation: fragmentation parameters are associated to the rule ID. Fragmentation is optional and feature "fragmentation" should be set. 


~~~~~
  grouping rule-id-type {
    leaf rule-id-value {
      type uint32;
      description
        "Rule ID value, this value must be unique combined with the length";
    }
    leaf rule-id-length {
      type uint8 {
        range "0..32";
      }
      description
        "Rule ID length in bits, value 0 is for implicit rules";
    }
    description
      "A rule ID is composed of a value and a length in bit";
  }

  // SCHC table for a specific device.

  container schc {
    list rule {
      key "rule-id-value rule-id-length";
      uses rule-id-type;
      choice nature {
        case fragmentation {
          if-feature "fragmentation";
          uses fragmentation-content;
        }
        case compression {
          uses compression-content;
        }
        case no-compression {
          description
            "RFC8724 allows a rule for uncompressed headers";
        }
        description
          "A rule is either for compression, no compression or fragmentation";
      }
      description
        "Set of rules compression, no compression or fragmentation rules 
        identified by their rule-id ";
    }
    description
      "a SCHC set of rules is composed of a list of rule which are either
       compression or fragmentation";
  }
}


~~~~~ 
{: #Fig-yang-schc title='Definition of a SCHC Context'}

To access to a specific rule, rule-id and its specific length is used as a key. The rule is either
a compression or a fragmentation rule.  

Each context can be identified though a version id. 

## Compression rule

A compression rule is composed of entries describing its processing (cf. {{Fig-comp-entry}}). An entry  contains all the information defined in {{Fig-ctxt}} with the types defined above. 

The compression rule described {{Fig-ctxt}} is defined by compression-content. It defines a list of
compression-rule-entry, indexed by their field id, position and direction. The compression-rule-entry 
element represent a line of the table {{Fig-ctxt}}. Their type reflects the identifier types defined in
{{comp_types}}

Some controls are made on the values:

* target value must be present for MO different from ignore.
* when MSB MO is specified, the matching-operator-value must be present

~~~~~ 
  grouping compression-rule-entry {
    description
      "These entries defines a compression entry (i.e. a line)
       as defined in RFC 8724 and fragmentation parameters.

       +-------+--+--+--+------------+-----------------+---------------+
       |Field 1|FL|FP|DI|Target Value|Matching Operator|Comp/Decomp Act|
       +-------+--+--+--+------------+-----------------+---------------+

       An entry in a compression rule is composed of 7 elements:
       - Field ID: The header field to be compressed. The content is a YANG identifer.
       - Field Length : either a positive integer of a function defined as a YANF id.
       - Field Position: a positive (and possibly equal to 0) integer.
       - Direction Indicator: a YANG identifier giving the direction.
       - Target value: a value against which the header Field is compared.
       - Matching Operator: a YANG id giving the operation, paramters may be
       associated to that operator.
       - Comp./Decomp. Action: A YANG id giving the compression or decompression
       action, paramters may be associated to that action.
      ";
    leaf field-id {
      type schc:fid-type;
      mandatory true;
      description
        "Field ID, identify a field in the header with a YANG refenceid.";
    }
    leaf field-length {
      type schc:fl-type;
      mandatory true;
      description
        "Field Length in bit or through a function defined as a YANG referenceid";
    }
    leaf field-position {
      type uint8;
      mandatory true;
      description
        "Field position in the header is a integer. If the field is not repeated
         in the header the value is 1, and incremented for each repetition of the field. Position
         0 means that the position is not important and order may change when decompressed";
    }
    leaf direction-indicator {
      type schc:di-type;
      mandatory true;
      description
        "Direction Indicator, a YANG referenceid to say if the packet is bidirectional,
         up or down";
    }
    list target-value {
      key "position";
      uses tv-struct;
      description
        "A list of value to compare with the header field value. If target value
         is a singleton, position must be 0. For matching-list, should be consecutive position
         values starting from 1.";
    }
    leaf matching-operator {
      type schc:mo-type;
      must "../target-value or derived-from-or-self(., 'mo-ignore')" {
        error-message "mo-equal, mo-msb and mo-match-mapping require target-value";
        description
          "target-value is not required for mo-ignore";
      }
      must "not (derived-from-or-self(., 'mo-msb')) or ../matching-operator-value" {
        error-message "mo-msb requires length value";
      }
      mandatory true;
      description
        "MO: Matching Operator";
    }
    list matching-operator-value {
      key "position";
      uses tv-struct;
      description
        "Matching Operator Arguments, based on TV structure to allow several arguments.
         In RFC 8724, only MSB define a single argument: length in bits  ";
    }
    leaf comp-decomp-action {
      type schc:cda-type;
      mandatory true;
      description
        "CDA: Compression Decompression Action";
    }
    list comp-decomp-action-value {
      key "position";
      uses tv-struct;
      description
        "CDA Arguments, based on TV structure to allow several arguments.
         In RFC 8724, no argument is defined for CDA";
    }
  }

  grouping compression-content {
    list entry {
      key "field-id field-position direction-indicator";
      uses compression-rule-entry;
      description
        "A compression rule is a list of rule entry describing
         each header field. An entry is identifed through a field-id, its position
         in the packet and its direction";
    }
    description
      "Define a compression rule composed of a list of entries.";
  }
~~~~~ 
{: #Fig-comp-entry title='Definition of a compression entry'}


## Fragmentation rule

A Fragmentation rule is composed of entries describing the protocol behavior. Some on them are numerical entries,
others are identifiers defined in {{frag_types}}.

The data model defines some relations between the entries:

* direction must be either up or down (not bidirectional).
* W size is only needed for Ack Always and Ack on Error modes.


~~~~~~
   grouping fragmentation-content {
    description
      "This grouping defines the fragmentation parameters for
       all the modes (No Ack, Ack Always and Ack on Error) specified in
       RFC 8724.";
    leaf l2-word-size {
      type uint8;
      default "8";
      description
        "Size in bit of the layer 2 word";
    }
    leaf direction {
      must "derived-from-or-self(., 'di-up') or derived-from-or-self(., 'di-down')" {
        error-message "direction for fragmentation rules is up or down";
      }
      type schc:direction-indicator-type;
      mandatory true;
      description
        "Should be up or down, bi directionnal is forbiden.";
    }
    leaf dtag-size {
      type uint8;
      default "0";
      description
        "Size in bit of the DTag field";
    }
    leaf w-size {
      when "not(derived-from(../fragmentation-mode, 'fragmentation-mode-no-ack'))";
      type uint8;
      description
        "Size in bit of the window field";
    }
    leaf fcn-size {
      type uint8;
      mandatory true;
      description
        "Size in bit of the FCN field";
    }
    leaf rcs-algorithm {
      type rcs-algorithm-type;
      default "schc:rcs-RFC8724";
      description
        "Algorithm used for RCS";
    }
    leaf maximum-window-size {
      type uint16;
      description
        "By default 2^wsize - 1";
    }
    leaf retransmission-timer {
      type uint64 {
        range "1..max";
      }
      description
        "Duration in seconds of the retransmission timer"; // Check the units
    }
    leaf inactivity-timer {
      type uint64;
      description
        "Duration is seconds of the inactivity timer, 0 indicates the timer is disabled"; // check units
    }
    leaf max-ack-requests {
      type uint8 {
        range "1..max";
      }
      description
        "The maximum number of retries for a specific SCHC ACK.";
    }
    leaf maximum-packet-size {
      type uint16;
      default "1280";
      description
        "When decompression is done, packet size must not strictly exceed this limit in Bytes";
    }
    leaf fragmentation-mode {
      type schc:fragmentation-mode-type;
      mandatory true;
      description
        "Which fragmentation mode is used (noAck, AckAlways, AckonError)";
    }
    choice mode {
      case no-ack;
      case ack-always;
      case ack-on-error {
        leaf tile-size {
          type uint8;
          when "derived-from(../fragmentation-mode, 'fragmentation-mode-ack-on-error')";
          description
            "Size in bit of tiles, if not specified or set to 0: tile fills the fragment.";
        }
        leaf tile-in-All1 {
          type schc:all1-data-type;
          when "derived-from(../fragmentation-mode, 'fragmentation-mode-ack-on-error')";
          description
            "When true, sender and receiver except a tile in All-1 frag";
        }
        leaf ack-behavior {
          type schc:ack-behavior-type;
          when "derived-from(../fragmentation-mode, 'fragmentation-mode-ack-on-error')";
          description
            "Sender behavior to acknowledge, after All-0, All-1 or when the
             LPWAN allows it (Always)";
        }
        leaf bitmap-format {
          type schc:bitmap-format-type;
          when "derived-from(../fragmentation-mode, 'fragmentation-mode-ack-on-error')";
          default "schc:bitmap-RFC8724";
          description
            "How the bitmaps are included in the Ack message.";
        }
      }
      description
        "RFC 8724 defines 3 fragmentation modes";
    }
  }
~~~~~~



## YANG Tree


~~~~~ 
module: ietf-schc
  +--rw schc
     +--rw rule* [rule-id-value rule-id-length]
        +--rw rule-id-value                 uint32
        +--rw rule-id-length                uint8
        +--rw (nature)?
           +--:(fragmentation) {fragmentation}?
           |  +--rw l2-word-size?           uint8
           |  +--rw direction               schc:di-type
           |  +--rw dtag-size?              uint8
           |  +--rw w-size?                 uint8
           |  +--rw fcn-size                uint8
           |  +--rw rcs-algorithm?          rcs-algorithm-type
           |  +--rw maximum-window-size?    uint16
           |  +--rw retransmission-timer?   uint64
           |  +--rw inactivity-timer?       uint64
           |  +--rw max-ack-requests?       uint8
           |  +--rw maximum-packet-size?    uint16
           |  +--rw fragmentation-mode      schc:fragmentation-mode-type
           |  +--rw (mode)?
           |     +--:(no-ack)
           |     +--:(ack-always)
           |     +--:(ack-on-error)
           |        +--rw tile-size?        uint8
           |        +--rw tile-in-All1?     schc:all1-data-type
           |        +--rw ack-behavior?     schc:ack-behavior-type
           |        +--rw bitmap-format?    schc:bitmap-format-type
           +--:(compression)
           |  +--rw entry* [field-id field-position direction-indicator]
           |     +--rw field-id                    schc:fid-type
           |     +--rw field-length                schc:fl-type
           |     +--rw field-position              uint8
           |     +--rw direction-indicator         schc:di-type
           |     +--rw target-value* [position]
           |     |  +--rw value?      binary
           |     |  +--rw position    uint16
           |     +--rw matching-operator           schc:mo-type
           |     +--rw matching-operator-value* [position]
           |     |  +--rw value?      binary
           |     |  +--rw position    uint16
           |     +--rw comp-decomp-action          schc:cda-type
           |     +--rw comp-decomp-action-value* [position]
           |        +--rw value?      binary
           |        +--rw position    uint16
           +--:(no-compression)

~~~~~ 
{: #Fig-model-overview title='Overview of SCHC data model}

# IANA Considerations

This document has no request to IANA.

# Security considerations {#SecConsiderations}

This document does not have any more Security consideration than the ones already raised on {{RFC8724}}

# Acknowledgements

The authors would like to thank Dominique Barthel, Carsten Bormann, Alexander Pelov. 

# YANG Module {#annexA}


~~~~
<code begins> file ietf-schc@2021-08-17.yang
{::include ietf-schc@2021-08-17.yang}
<code ends>
~~~~
{: #Fig-schc title="SCHC data model}


--- back
