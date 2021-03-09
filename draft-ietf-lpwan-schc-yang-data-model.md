---
stand_alone: true
ipr: trust200902
docname: draft-ietf-lpwan-schc-yang-data-model-04
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
    I-D.ietf-lpwan-coap-static-context-hc:
    I-D.barthel-lpwan-oam-schc:
    RFC7252:
    
--- abstract

This document describes a YANG data model for the SCHC (Static Context Header Compression) 
compression and fragmentation rules.

--- middle

# Introduction {#Introduction}

# SCHC rules

SCHC is a compression and fragmentation mechanism for constrained networks defined in {{RFC8724}}.
It is based on a static context shared by two entities at the boundary this constrained network.
Draft {{RFC8724}} provides a non formal representation of the rules used either for compression/decompression (or C/D)
or fragmentation/reassembly (or F/R). The goal of this document is to formalize the description of the rules to offer:

* the same definition on both ends, even if the internal representation is different. 
* an update the other end to set up some specific values (e.g. IPv6 prefix, Destination address,...)
* ...

This document defines a YANG module to represent both compression and fragmentation rules, which leads to a common representation for all the rules elements. 

SCHC compression is generic, its mechanism does no refer
to a specific protocol. Any packet header field is described by an ID, a position, a flow direction and a value, which can be a numerical
value or a string. {{RFC8724}} and {{I-D.ietf-lpwan-coap-static-context-hc}} specify compression of IPv6, UDP, CoAP and OSCORE fields. {{I-D.barthel-lpwan-oam-schc}} decribes ICMPv6 header compression.

SCHC fragmentation requires a set of common parameters that are included in a rule. These parameters are defined in {{RFC8724}}.


## Compression Rules

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

##Field Identifier

Before compression is attempted, the headers of the original packet are first parsed and a list of fields is built. This list of fields
is matched against the fields in the compression rules, in order to find a rule valid for compressing that packet header.
The correspondance between the elements of the parsed packet headers list and the elements of the rule fields 
is done via the Field ID.  {{RFC8724}}  does not state how the Field ID value is constructed. 
In the examples provided in {{RFC8724}}, Field IDs are represented as strings, with field names prepended with the protocol name (e.g. IPv6.version, CoAP.version,...).

In the YANG model specified here, each field MUST be identified through a global YANG identityref. A YANG Field ID  derives from the field-id-base-type. {{Fig-ex-field-id}} gives some Field ID definitions. Note that some fields can be broken down into smaller pieces. This is the case for "fid-ipv6-trafficclass-ds" and "fid-ipv6-trafficclass-ecn" which are a subset of "fid-ipv6-trafficclass-ds".


~~~~~

   identity field-id-base-type  {
  	   description "Field ID with SID";
    }

    identity fid-ipv6-version {
  	   base field-id-base-type;
	   description "IPv6 version field from RFC8200";
    }

  identity fid-ipv6-trafficclass {
  	   base field-id-base-type;
	   description "IPv6 Traffic Class field from RFC8200";
  }

  identity fid-ipv6-trafficclass-ds {
  	   base field-id-base-type;
	   description "IPv6 Traffic Class field from RFC8200, 
       DiffServ field from RFC3168";
  }

  identity fid-ipv6-trafficclass-ecn {
  	   base field-id-base-type;
	   description "IPv6 Traffic Class field from RFC8200, 
       ECN field from RFC3168";
  }
  
  ...

~~~~~
{: #Fig-ex-field-id title='Definition of identityref for some IPv6 fields'}

{{Fig-ex-field-id}} gives some examples of field identityref definitions. The base identity is field-id-base-type, and field id are derived for it. 

The naming convention is "fid" followed by the protocol name and the field name.  
The yang model in annex (see {{annexA}}) gives the full definition of the Field ID for {{RFC8724}}, {{I-D.ietf-lpwan-coap-static-context-hc}}, and {{I-D.barthel-lpwan-oam-schc}}.

The type associated to this identity is field-id-type (cf. {{Fig-field-id-type}})

~~~~~
    typedef field-id-type {
        description "Field ID generic type.";
        type identityref {
            base field-id-base-type;
        }
    }
~~~~~
{: #Fig-field-id-type title='Type definition for field IDs'}

<!--
### CoAP options

Option in COAP are specified by several documents. To avoid to add a yang specification each time a new option is defined, this document preallocated a block 
of 255 identityref corresponding to the two first blocks described in Table 8 of {{RFC7252}}. 
-->

## Field length 

Field length is either an integer giving the size of a field in bits or a specific function. {{RFC8724}} defines the
"var" function which applies to byte-based variable length fields and {{I-D.ietf-lpwan-coap-static-context-hc}} defines the "tkl" function dedicated for managing the CoAP
Token field, which is also of variable length.

~~~~~

  identity field-length-base-type {
        description "used to extend field length functions";
  }

  identity fl-variable {
  	   base field-length-base-type;
	   description "residue length in Byte is sent";
  }

  identity fl-token-length {
  	   base field-length-base-type;
	   description "residue length in Byte is sent";
  }

~~~~~
{: #Fig-ex-field-length title='Definition of identityref for field length'}

As for Field ID, the Field Length function can be defined as a identityref as shown in {{Fig-ex-field-length}}.

Therefore, the type of Field Length is a union between an integer, expressing (in number of bits) the length of fixed-length fields, and the identityref (cf. {{Fig-ex-field-length-union}}).

~~~~~
    typedef field-length-type {
        description "Field length, either as a positive integer expressing the size in bits 
        or a function defined through an identityref.";
        type union {
            type int64; /* positive length in bits */
            type identityref { /* function */
                base field-length-base-type;
            }
        }
    }
~~~~~
{: #Fig-ex-field-length-union title='Type definition for Field Length'}

The naming convention is fl followed by the function name as defined in SCHC specifications. 

## Field position

Field Position is a positive integer, which describes the ordinal position of a field in a header.
The default value is 1, but for fields that appear multiple times in a header, the value may be larger. 
The value 0 indicates that the position is not to be taken into account for the rule selection process. 

Field position is a positive integer. The type is an uint8.

## Direction Indicator

The Direction Indicator (DI) is used to tell if a rule field applies to both flow directions (Bi) or only to uplink (Up) or downlink (Dw) flows. 

~~~~~

  identity direction-indicator-base-type {
        description "used to extend field length functions";
  }

  identity di-bidirectional {
  	   base direction-indicator-base-type;
	   description "Direction Indication of bi directionality";
  }

  identity di-up {
  	   base direction-indicator-base-type;
	   description "Direction Indication of upstream";
  }

  identity di-down {
  	   base direction-indicator-base-type;
	   description "Direction Indication of downstream";
  }

~~~~~
{: #Fig-ex-field-DI title='Definition of identityref for direction indicators'}

{{Fig-ex-field-DI}} gives the identityref for Direction Indicators.

The type is "direction-indicator-type" (cf. {{Fig-field-DI-type}}).

~~~~~
    typedef direction-indicator-type {
        description "direction in LPWAN network, up when emitted by the device,
        down when received by the device, bi for either direction.";
        type identityref {
            base direction-indicator-base-type;
        }
    }
~~~~~
{: #Fig-field-DI-type title='Type definition for direction indicators'}

## Target Value

A Target Value may be a string or a binary sequence, or even a list of these (when used with the match-mapping operator).
To encompass all these cases, Target Value is defined in the data model as a list of position and values, where position is the index in the list.
By default, the position is set to 0.

The leaf "value" is not mandatory to represent a non existing value in a TV.

~~~~~
    grouping target-values-struct {
        description "defines the target value element. Can be either an arbitrary
        binary or ascii element. All target values are considered as matching lists.
        Position is used to order values, by default position 0 is used when containing
        a single element.";

        leaf value {
            type union {
                type binary;
                type string;
            }
        }
        leaf position {
            description "If only one element position is 0, otherwise position is the
            matching list.";
            type uint16;
        }
    }
~~~~~
{: #Fig-ex-TV title='Definition of target value'}

{{Fig-ex-TV}} shows the definition of a single element of a Target Value.
In a compression rule, this will be used as a list, with position as the index.
The index sent as part of the compression residue is expressed on the minimal number of bits needed to represented the maximum index.


## Matching Operator

Matching Operator (MO) is a function applied to decide of a match between a field value (from the parsed protocol header) and the rule target value. {{RFC8724}} defines 4 MO.

~~~~~
   identity matching-operator-base-type {
      description "used to extend Matching Operators with SID values";
   }

   identity mo-equal {
      base matching-operator-base-type;
      description "RFC 8724";
   }
   
   identity mo-ignore {
      base matching-operator-base-type;
      description "RFC 8724";
   }
   
   identity mo-msb {
      base matching-operator-base-type;
      description "RFC 8724";
   }
   
   identity mo-matching {
      base matching-operator-base-type;
      description "RFC 8724";
   }
~~~~~
{: #Fig-ex-MO title='Definition of identityref for Matching Operator '}

The type is "matching-operator-type" (cf. {{Fig-MO-type}})

~~~~~
    typedef matching-operator-type {
        description "Matching Operator (MO) to compare fields values with target values";
        type identityref {
            base matching-operator-base-type;
        }
    }
~~~~~
{: #Fig-MO-type title='Type definition for Matching Operator'}

### Matching Operator arguments

Some Matching Operators, (e.g., MSB()) take arguments.
Even if MSB() is currently the only MO to take arguments, and actually only one argument, in the future more MOs may be defined and some may require several arguments.
They are viewed as a list of target-values-type.

## Compression Decompression Actions

Compression Decompression Action (CDA) identifies the pair of functions to use for compression or decompression. 
{{RFC8724}} defines 7 CDA. 

~~~~~
     identity compression-decompression-action-base-type;

    identity cda-not-sent {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   

    identity cda-value-sent {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   

    identity cda-lsb {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   

    identity cda-mapping-sent {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   

    identity cda-compute-* {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   

    identity cda-deviid {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   

   identity cda-appiid {
    	base compression-decompression-action-base-type;
	    description "RFC 8724";
    }   
~~~~~
{: #Fig-ex-CDA title='Definition of identityref for  Compresion Decompression Action'}

The type is "comp-decomp-action-type" (cf. {{Fig-CDA-type}})

~~~~~
   typedef comp-decomp-action-type {
        description "Compression Decompression Action to compression or decompress a field.";
        type identityref {
            base compression-decompression-action-base-type;
        }
    }

~~~~~
{: #Fig-CDA-type title='Type definition for Compresion Decompression Action'}

### Compression Decompression Action arguments

Currently no CDA requires arguments, but some future CDA may require one or several arguments.
They are viewed as a list of target-values-type.

# Rule definition

A rule is either a C/D or an F/R rule. A rule is identified by the value of Rule ID and the number of bits it is represented on.
The YANG grouping rule-id-type defines the structure used to represent a Rule ID. A zero length is allowed, it represents an implicit rule. 

~~~~~
// Define rule ID. Rule ID is composed of a RuleID value and a Rule ID Length

    grouping rule-id-type {
        leaf rule-id {
            type uint32;
            description "rule ID value, this value must be unique combined with the length";
        }
        leaf rule-length {
            type uint8 {
                range 0..32;
            }
            description "rule ID length in bits, value 0 is for implicit rules";
        }
    }

// SCHC table for a specific device.

    container schc {
        leaf version{
            type uint64;
            mandatory false;
            description "used as an indication for versioning";
        }
        list rule {
            key "rule-id rule-length";
            uses rule-id-type;
            choice nature {
                case fragmentation {
                    uses fragmentation-content;
                }
                case compression {
                    uses compression-content;
                }
            }
        }
    }
  

~~~~~ 
{: #Fig-yang-schc title='Definition of a SCHC Context'}

To access a specific rule in a set of rules, Rule ID and its associated length are used as a key. The rule is either
a compression or a fragmentation rule.  

Each context can be identified though a version id. 

## Compression rule

A compression rule is composed of entries describing its processing (cf. {{Fig-comp-entry}}). An entry  contains all the information defined in {{Fig-ctxt}} with the types defined above. 

### Compression context representation.

The compression rule described in {{Fig-ctxt}} is associated with a Rule ID. The compression
rule entry is defined in  {{Fig-comp-entry}}. Each column in the table
is either represented by a leaf or a list. Note that Matching Operators and Compression 
Decompression Actions can have arguments. These are viewed as ordered list of strings and numbers,
much like target values.

~~~~~ 
    grouping compression-rule-entry {
        description "These entries defines a compression entry (i.e. a line) 
        as defined in RFC 8724 and fragmentation parameters.
  
        +-------+--+--+--+------------+-----------------+---------------+
        |Field 1|FL|FP|DI|Target Value|Matching Operator|Comp/Decomp Act|
        +-------+--+--+--+------------+-----------------+---------------+

        An entry in a compression rule is composed of 7 elements:
        - Field ID: The header field to be compressed. The content is a YANG identifer.
        - Field Length : either a positive integer of a function defined as a YANG id.
        - Field Position: a positive (and possibly equal to 0) integer.
        - Direction Indicator: a YANG identifier giving the direction.
        - Target value: a value against which the header Field is compared.
        - Matching Operator: a YANG id giving the operation, parameters may be 
        associated to that operator.
        - Comp./Decomp. Action: A YANG id giving the compression or decompression
        action, parameters may be associated to that action.  
        ";

        leaf field-id {
            description "Field ID, identify a field in the header with a YANG identityref.";
            mandatory true;
            type schc:field-id-type;
        }
        leaf field-length {
            description "Field Length in bit or through a function defined as a YANG identityref";
            mandatory true;
            type schc:field-length-type;
        }
        leaf field-position {
            description "field position in the header is a integer. If the field is not repeated 
            in the header the value is 1, and incremented for each repetition of the field. Position
            0 means that the position is not important and order may change when decompressed"; 
            mandatory true;
            type uint8; 
        }
        leaf direction-indicator {
            description "Direction Indicator, a YANG identityref to say if the packet is bidirectionnal,
            up or down";
            mandatory true;
            type schc:direction-indicator-type;
        }
        list target-values {
            description "a list of value to compare with the header field value. If target value
            is a singleton, position must be 0. For matching-list, should be consecutive position
            values starting from 1.";
            key position;
            uses target-values-struct;
        }
        leaf matching-operator {
            mandatory true;
            type schc:matching-operator-type;
        }
        list matching-operator-value {
            key position;
            uses target-values-struct;
        }
        leaf comp-decomp-action {
            mandatory true;
            type schc:comp-decomp-action-type;
        }
        list comp-decomp-action-value {
            key position;
            uses target-values-struct;
        }
    }
~~~~~ 
{: #Fig-comp-entry title='Definition of a compression entry'}

### Rule definition

A compression rule is a list of entries. 

~~~~~ 
    grouping compression-content {
        description "define a compression rule composed of a list of entries.";
        list entry {
            key "field-id field-position direction-indicator"; 
            uses compression-rule-entry;
        }
    }
~~~~~ 
{: #Fig-comp-rule title='Definition of a compression rule'}

To identify a specific entry Field ID, position and direction are needed.


## Fragmentation rule

Parameters for fragmentation are defined in Annex D of {{RFC8724}}. 


{{Fig-frag-header}} gives the first elements found in this structure. It starts with 
a direction. Since fragmentation rules only apply to a specific flow direction, they MUST contain a direction.
Its type is the same as the one used for compression rule entries, but the use of bidirectionnal is 
forbidden. 

The next elements describe the size of SCHC fragmentation header fields. Only the FCN size is mandatory
and its value must be greater or equal to 1. 

~~~~~ 
    grouping fragmentation-content {
        description "This grouping defines the fragmentation parameters for
        all the modes (No Ack, Ack Always and Ack on Error) specified in 
        RFC 8724.";

        leaf direction {
            type schc:direction-indicator-type;
            description "should be up or down, bi directionnal is forbidden.";
            mandatory true;
        }
        leaf dtagsize {
            type uint8;
            description "size in bit of the DTag field";

        }
        leaf wsize {
            type uint8;
            description "size in bit of the window field";
        }
        leaf fcnsize {
            type uint8 {
                range 1..max;
            }
            description "size in bit of the FCN field";
            mandatory true;
        }
...
~~~~~ 
{: #Fig-frag-header title='Definition of a fragmentation parameters, SCHC header'}

The default RCS algorithm is defined to be the CRC computation proposed in {{RFC8724}} (see {{Fig-frag-header2}}).
Other RCS algorithms are identified through an identityref specified in the SCHC Data Model and with the type RCS-algorithm-type ({{Fig-ex-RCS}}).


~~~~~ 
...
        leaf RCS-algorithm {
            type RCS-algorithm-type;
            default schc:RFC8724-RCS;
            description "Algoritm used for RCS";
        }
...
~~~~~ 
{: #Fig-frag-header2 title='Definition of a fragmentation parameters, RCS algorithm'}

~~~~~
    identity RCS-algorithm-base-type {
        description "identify which algorithm is used to compute RSC.
        The algorithm defines also the size if the RSC field.";
    }

    identity RFC8724-RCS {
        description "CRC 32 defined as default RCS in RFC8724.";
        base RCS-algorithm-base-type;
    }

    typedef RCS-algorithm-type {
        type identityref {
            base RCS-algorithm-base-type;
        }
    }
~~~~~
{: #Fig-ex-RCS title='Definition of identityref for RCS Algorithm'}

{{Fig-frag-header3}} gives the parameters used by the state machine to handle fragmentation:

* maximum-window-size contains the maximum FCN value that can be used. 
* retransmission-timer gives in seconds the duration before sending an ack request (cf. section 8.2.2.4. of {{RFC8724}}). If specifed, value must be higher or equal to 1. 
* inactivity-timer gives in seconds the duration before aborting (cf. section 8.2.2.4. of {{RFC8724}}). The value 0 explicitly indicates that this timer is disabled.
* max-ack-requests gives the number of attempts before aborting (cf. section 8.2.2.4. of {{RFC8724}}).
* maximum-packet-size gives in bytes the larger packet size that can be reassembled. 

~~~~~
...
        leaf maximum-window-size {
            type uint16;
            description "by default 2^wsize - 2";
        }

        leaf retransmission-timer {
            type uint64 {
                range 1..max;
            }
            description "duration in seconds of the retransmission timer"; // Check the units
        }

        leaf inactivity-timer {
            type uint64;
            description "duration is seconds of the inactivity timer, 0 indicates the timer is disabled"; // check units
        }

        leaf max-ack-requests {
            type uint8 {
                range 1..max;
            }
            description "the maximum number of retries for a specific SCHC ACK.";        
        }

        leaf maximum-packet-size {
            type uint16;
            default 1280;
            description "When decompression is done, packet size must not strictly exceed this limit in Bytes";
        }
...
~~~~~
{: #Fig-frag-header3 title='Definition of a fragmentation state machine parameters'}

{{Fig-frag-header4}} gives information related to a specific fragmentation mode: fragmentation-mode MUST be set with a specific behavior. Identityref are given {{Fig-frag-AoE-val}}. 

For Ack on Error some specific information may be provided:

* tile-size gives in bits the size of the tile; If set to 0 a single tile is inserted inside a fragment.
* tile-in-All1 indicates if All1 contains only the RCS (all1-data-no) or may contain a single tile (all1-data-yes). Since the reassembly process may detect this behavior, the choice can be left to the fragmentation process. In that case identityref all1-data-sender-choice has to be specified. All possible values are given {{Fig-frag-AoE-val}}.  
* ack-behavior tells when the fragmentation process may send acknowledgments. When ack-behavior-after-All0 is specified, the ack may be sent after the reception of All-0 fragment. When ack-behavior-after-All1 is specified, the ack may be sent after the reception of All-1 fragment at the end of the fragmentation process.  ack-behavior-always do not impose a limitation at the SCHC level. The constraint may come from the LPWAN technology.  All possible values are given {{Fig-frag-AoE-val}}.  

~~~~~
...
        leaf fragmentation-mode {
            type schc:fragmentation-mode-type;
            description "which fragmentation mode is used (noAck, AckAlways, AckonError)";
            mandatory true;
        }

        choice mode {
            case no-ack;
            case ack-always;
            case ack-on-error {
                leaf tile-size {
                    type uint8;
                    description "size in bit of tiles, if not specified or set to 0: tile fills the fragment.";
                }
                leaf tile-in-All1 {
                    type schc:all1-data-type;
                    description "When true, sender and receiver except a tile in All-1 frag";
                }
                leaf ack-behavior {
                    type schc:ack-behavior-type;
                    description "Sender behavior to acknowledge, after All-0, All-1 or when the
                    LPWAN allows it (Always)";
                }
            }
       }
...
~~~~~ 
{: #Fig-frag-header4 title='Definition of a fragmentation specific information'}

~~~~~
// -- FRAGMENTATION TYPE

// -- fragmentation modes

    identity fragmentation-mode-base-type {
        description "fragmentation mode";
    }

    identity fragmentation-mode-no-ack {
        description "No Ack of RFC 8724.";
        base fragmentation-mode-base-type;
    }

    identity fragmentation-mode-ack-always {
        description "Ack Always of RFC8724.";
        base fragmentation-mode-base-type;
    }
    identity fragmentation-mode-ack-on-error {
        description "Ack on Error of RFC8724.";
        base fragmentation-mode-base-type;
    }

    typedef fragmentation-mode-type {
        type identityref {
            base fragmentation-mode-base-type;
        }
    }
    
// -- Ack behavior 

    identity ack-behavior-base-type {
        description "define when to send an Acknowledgment message";
    }

    identity ack-behavior-after-All0 {
        description "fragmentation expects Ack after sending All0 fragment."; 
        base ack-behavior-base-type;
    }

    identity ack-behavior-after-All1 {
        description "fragmentation expects Ack after sending All1 fragment.";
        base ack-behavior-base-type;
    }

    identity ack-behavior-always {
        description "fragmentation expects Ack after sending every fragment.";
        base ack-behavior-base-type;
    }

    typedef ack-behavior-type {
        type identityref {
            base ack-behavior-base-type;
        }
    }

// -- All1 with data types

    identity all1-data-base-type {
        description "type to define when to send an Acknowledgment message";
    }

    identity all1-data-no {
        description "All1 contains no tiles."; 
        base all1-data-base-type;
    }

    identity all1-data-yes {
        description "All1 MUST contain a tile";
        base all1-data-base-type;
    }

    identity all1-data-sender-choice {
        description "Fragmentation process choose to send tiles or not in all1.";
        base all1-data-base-type;
    }

    typedef all1-data-type {
        type identityref {
            base all1-data-base-type;
        }
    }


~~~~~ 
{: #Fig-frag-AoE-val title='Specific types for Ack On Error mode'}
## YANG Tree


~~~~~ 
module: schc
  +--rw schc
     +--rw version?   uint64
     +--rw rule* [rule-id rule-length]
        +--rw rule-id                       uint32
        +--rw rule-length                   uint8
        +--rw (nature)?
           +--:(fragmentation)
           |  +--rw direction               schc:direction-indicator-type
           |  +--rw dtagsize?               uint8
           |  +--rw wsize?                  uint8
           |  +--rw fcnsize                 uint8
           |  +--rw RCS-algorithm?          RCS-algorithm-type
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
           +--:(compression)
              +--rw entry* [field-id field-position direction-indicator]
                 +--rw field-id                    schc:field-id-type
                 +--rw field-length                schc:field-length-type
                 +--rw field-position              uint8
                 +--rw direction-indicator         schc:direction-indicator-type
                 +--rw target-values* [position]
                 |  +--rw value?      union
                 |  +--rw position    uint16
                 +--rw matching-operator           schc:matching-operator-type
                 +--rw matching-operator-value* [position]
                 |  +--rw value?      union
                 |  +--rw position    uint16
                 +--rw comp-decomp-action          schc:comp-decomp-action-type
                 +--rw comp-decomp-action-value* [position]
                    +--rw value?      union
                    +--rw position    uint16

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
<code begins> file schc@2020-06-15.yang
{::include schc@2020-06-15.yang}
<code ends>
~~~~
{: #Fig-schc title="SCHC data model}


--- back
