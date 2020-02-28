---
stand_alone: true
ipr: trust200902
docname: draft-ietf-lpwan-schc-yang-data-model-03
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
    I-D.ietf-lpwan-ipv6-static-context-hc:
    I-D.ietf-lpwan-coap-static-context-hc:
    RFC7252:
    
--- abstract

This document describes a YANG data model for the SCHC (Static Context Header Compression) 
compression and fragmentation rules.

--- middle

# Introduction {#Introduction}

# SCHC rules

SCHC is a compression and fragmentation mechanism for constrained networks defined in {{I-D.ietf-lpwan-ipv6-static-context-hc}} 
it is based on a static context shared by two entities at the boundary this contrained network.
Draft {{I-D.ietf-lpwan-ipv6-static-context-hc}} provides an abstract representation of the rules used either for compression/decompression (or C/D)
or fragmentation/reassembly (or F/R). The goal of this document is to formalize the description of the rules to offer:

*  universal representation of the rule to allow the same rule represention on both ends. For instance; a device 
   can provide the rule it uses to store them in the core SCHC C/D and F/R. 
*  a device or the core SCHC instance may update the other end to set upsome specific values 
   (e.g. IPv6 prefix, Destination address,...)
* ...

This document defines a YANG module to represent both compression and fragmentation rules, which leads to common 
representation and values for the elements of the rules. SCHC compression is generic, the main mechanism do no refers
to a specific fields. A field is abstractedh through an ID, a position, a direction and a value that can be a numerical
value or a string.

{{I-D.ietf-lpwan-ipv6-static-context-hc}} and {{I-D.ietf-lpwan-coap-static-context-hc}} specifies fields for IPv6, UDP, CoAP and OSCORE. 

Fragmentation requires a set of common parameters that are included in a rule.


## Compression Rules

{{I-D.ietf-lpwan-ipv6-static-context-hc}} proposes an abstract representation of the compression rule.
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

In the process of compression, the headers of the original packet are first parsed to create a list of fields. This list of fields
is matched again the rules to find the appropriate one and apply compression. The link between the list given by the parsed fields and the
rules is doen through a field ID.  {{I-D.ietf-lpwan-ipv6-static-context-hc}}  do not state how the field ID value can be constructed. 
In the given example, it was given through a string indexed by the protocol name (e.g. IPv6.version, CoAP.version,...).

Using the YANG model, each field can be identified through a global YANG identityref. A YANG field ID  derives from the field-id-base-type. {{Fig-ex-field-id}} gives some field ID definitions. Note that some field IDs can be splitted is smaller pieces. This is the case for "fid-ipv6-trafficclass-ds" and "fid-ipv6-trafficclass-ecn" which are a subset of "fid-ipv6-trafficclass-ds".


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

  identity fid-coap-option-if-match {
  	  base field-id-base-type;
	    description "CoAP option If-Match from RFC 7252";
  }

  identity fid-coap-option-uri-host {
  	  base field-id-base-type;
	    description "CoAP option URI-Host from RFC 7252";
  }
  
  ...

~~~~~
{: #Fig-ex-field-id title='Definition of indentityref for field IDs'}

{{Fig-ex-field-id}} gives an example of field ID identityref definitions. The base identity is field-id-base-type, and field id are derived for it.
The naming convention is "fid" followed by the protocol name and the field name.  
The yang model in annex gives the full definition of the field ID for {{I-D.ietf-lpwan-ipv6-static-context-hc}} and {{I-D.ietf-lpwan-coap-static-context-hc}}.

The type associated to this identity is field-id-type (cf. {{Fig-field-id-type}})

~~~~~
    typedef field-id-type {
        description "Field ID generic type.";
        type identityref {
            base field-id-base-type;
        }
    }
~~~~~
{: #Fig-field-id-type title='Definition of indentityref for field IDs'}

<!--
### CoAP options

Option in COAP are specified by several documents. To avoid to add a yang specification each time a new option is defined, this document preallocated a block 
of 255 identityref corresponding to the two first blocks described in Table 8 of {{RFC7252}}. 
-->

## Field length 

Field length is either an integer giving the size of a field in bits or a function. {{I-D.ietf-lpwan-ipv6-static-context-hc}} defines the
"var" function which allows variable length fields in byte and {{I-D.ietf-lpwan-coap-static-context-hc}} defines the "tkl" function for managing the CoAP
Token length field.

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
{: #Fig-ex-field-length title='Definition of indetntyref for field IDs'}

As for field ID, field length function can be defined as a identityref as shown in {{Fig-ex-field-length}}.

Therefore the type for field length is a union between an integer giving in bits the size of the length and the identityref (cf. {{Fig-ex-field-length-union}}).

~~~~~
    typedef field-length-type {
        type union {
            type int64; /* positive length */
            type identityref { /* function */
                base field-length-base-type;
            }
        }
    }
~~~~~
{: #Fig-ex-field-length-union title='Definition of indetntyref for field IDs'}

The naming convention is fl followed by the function name as defined in SCHC specifications. 



## Field position

Field position is a positive integer which gives the position of a field, the default value is 1, but if the field is repeated several times, the value is higher. 
value 0 indicates that the position is not important and is not taken into account during the rule selection process. 

Field position is a positive integer. The type is an uint8.

## Direction Indicator

The Direction Indicator (DI) is used to tell if a field appears in both direction (Bi) or only uplink (Up) or Downlink (Dw). 

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
        type identityref {
            base direction-indicator-base-type;
        }
    }
~~~~~
{: #Fig-field-DI-type title='Definition of identityref for direction indicators'}

## Target Value

Target Value may be either a string or binary sequence. For match-mapping, several of these values can 
be contained in a Target Value field. In the data model, this is generalized by adding a position, which
orders the list of values. By default the position is set to 0.

The leaf "value" is not mandatory to represent a non existing value in a TV.

~~~~~

  grouping target-values-struct {
    leaf value {
      type union {
        type binary;
        type string;
      }
    }
    leaf position {
          type uint16;
    }
  }

~~~~~
{: #Fig-ex-TV title='Definition of target value'}

{{Fig-ex-TV}} gives the definition of a single element of a Target Value. In the rule, this will be used as a list, with position as a key.


## Matching Operator

Matching Operator (MO) is a function applied between a field value provided by the parsed header and the target value. {{I-D.ietf-lpwan-ipv6-static-context-hc}} defines 4 MO.

~~~~~
   identity matching-operator-base-type {
      description "used to extend Matching Operators with SID values";
   }

   identity mo-equal {
      base matching-operator-base-type;
      description "SCHC draft";
   }
   
   identity mo-ignore {
      base matching-operator-base-type;
      description "SCHC draft";
   }
   
   identity mo-msb {
      base matching-operator-base-type;
      description "SCHC draft";
   }
   
   identity mo-matching {
      base matching-operator-base-type;
      description "SCHC draft";
   }
~~~~~
{: #Fig-ex-MO title='Definition of Matching Operator identity'}

the type is "matching-operator-type" (cf. {{Fig-MO-type}})

~~~~~
   typedef matching-operator-type {
        type identityref {
            base matching-operator-base-type;
        }
    }
~~~~~
{: #Fig-MO-type title='Definition of Matching Operator type'}

### Matching Operator arguments

Some Matching Operator such as MSB can take some values. Even if currently LSB is the only MO takes only one argument, in the future some MO may require several arguments.
They are viewed as a list of target-values-type.

## Compression Decompresison Actions

Compresion Decompression Action (CDA) idenfied the function to use either for compression or decompression. 
{{I-D.ietf-lpwan-ipv6-static-context-hc}} defines 6 CDA. 

~~~~~

    identity compression-decompression-action-base-type;

    identity cda-not-sent {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

    identity cda-value-sent {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

    identity cda-lsb {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

    identity cda-mapping-sent {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

    identity cda-compute-length {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

    identity cda-compute-checksum {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

    identity cda-deviid {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }   

   identity cda-appiid {
    	base compression-decompression-action-base-type;
	   description "from SCHC draft";
    }    

~~~~~
{: #Fig-ex-CDA title='Definition of Compresion Decompression Action identity'}

The type is "comp-decomp-action-type" (cf. {{Fig-CDA-type}})

~~~~~
   typedef comp-decomp-action-type {
        type identityref {
            base compression-decompression-action-base-type;
        }
    }

~~~~~
{: #Fig-CDA-type title='Definition of Compresion Decompression Action type'}

### Compression Decompression Action arguments

Currently no CDA requires argumetns, but the future some CDA may require several arguments.
They are viewed as a list of target-values-type.

# Rule definition

A rule is either a C/D or an F/R rule. A rule is identified by the rule ID value and its associated length. The YANG grouping rule-id-type defines the structure used to represent a rule ID. Length of 0 is allowed to represent an implicit rule. 

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

To access to a specfic rule, rule-id and its specific length is used as a key. The rule is either
a compression or a fragmentation rule.  

Each context can be identify though a version id. 

## Compression rule

A compression rule is composed of entries describing its processing (cf. {{Fig-comp-entry}}). An entry  contains all the information defined in {{Fig-ctxt}} with the types defined above. 

### Compression context representation.

The compression rule described {{Fig-ctxt}} is associated to a rule ID. The compression
rule entry is defined in  {{Fig-comp-entry}}. Each column in the table
is either represented by a leaf or a list. Note that Matching Operators and Compression 
Decompression actions can have arguments. They are viewed a ordered list of strings and numbers
as in target values.

~~~~~ 
    grouping compression-rule-entry {
        leaf field-id {
            mandatory true;
            type schc-id:field-id-type;
        }
        leaf field-length {
            mandatory true;
            type schc-id:field-length-type;
        }
        leaf field-position {
            mandatory true;
            type uint8; 
        }
        leaf direction-indicator {
            mandatory true;
            type schc-id:direction-indicator-type;
        }
        list target-values {
            key position;
            uses target-values-struct;
        }
        leaf mo {
            mandatory true;
            type schc-id:matching-operator-type;
        }
        list mo-value {
            key position;
            uses target-values-struct;
        }
        leaf cda {
            mandatory true;
            type schc-id:comp-decomp-action-type;
        }
        list cda-value {
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
    list entry {
        key "field-id field-position direction-indicator"; 
	      uses compression-rule-entry;
    }
  }
~~~~~ 
{: #Fig-comp-rule title='Definition of a compression rule'}

To identify a specific entry Field ID, position and direction are needed.


## Fragmentation rule

Parameters for fragmentation are defined in Annex D of {{I-D.ietf-lpwan-ipv6-static-context-hc}}. 
Two new types are defined for Ack on Error acknowlement behavior (ack-behavior-type) and the RCS 
algorithm (RCS-algorithm-type).

~~~~~ 
    grouping fragmentation-content {
        leaf direction {
            type schc-id:direction-indicator-type;
            description "should be up or down";
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
            type uint8;
            description "size in bit of the FCN field";
        }
        leaf RCS-algorithm {
            type RCS-algorithm-type;
            default schc-id:RFC8724-RCS;
            description "Algoritm used for RCS";
        }
        leaf maximum-window-size {
            type uint16;
            description "by default 2^wsize - 1";
        }

        leaf retransmission-timer {
            type uint64;
            description "duration in seconds of the retransmission timer"; // Check the units
        }

        leaf inactivity-timer {
            type uint64;
            description "duration is seconds of the inactivity timer"; // check units
        }

        leaf max-ack-requests {
            type uint8;        
        }

        leaf maximum-packet-size {
            type uint16;
            mandatory true;
            default 1280;
            description "When decompression is done, packet size must not strictly exceed this limit in Bytes";
        }

        choice mode {
            case no-ack;
            case ack-always;
            case ack-on-error {
                leaf tile-size {
                    type uint8;
                    description "size in bit of tiles";
                }
                leaf tile-in-All1 {
                    type boolean;
                    description "When true, sender and receiver except a tile in All-1 frag";
                }
                leaf ack-behavior {
                    type schc-id:ack-behavior-type;
                    mandatory true;
                }

            }
       }
    }
~~~~~ 
{: #Fig-frag-rule title='Definition of a fragmentation rule'}

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
           |  +--rw direction?              schc-id:direction-indicator-type
           |  +--rw dtagsize?               uint8
           |  +--rw wsize?                  uint8
           |  +--rw fcnsize?                uint8
           |  +--rw RCS-algorithm?          RCS-algorithm-type
           |  +--rw maximum-window-size?    uint16
           |  +--rw retransmission-timer?   uint64
           |  +--rw inactivity-timer?       uint64
           |  +--rw max-ack-requests?       uint8
           |  +--rw maximum-packet-size     uint16
           |  +--rw (mode)
           |     +--:(no-ack)
           |     +--:(ack-always)
           |     +--:(ack-on-error)
           |        +--rw tile-size?        uint8
           |        +--rw tile-in-All1?     boolean
           |        +--rw ack-behavior      schc-id:ack-behavior-type
           +--:(compression)
              +--rw entry* [field-id field-position direction-indicator]
                 +--rw field-id               schc-id:field-id-type
                 +--rw field-length           schc-id:field-length-type
                 +--rw field-position         uint8
                 +--rw direction-indicator    schc-id:direction-indicator-type
                 +--rw target-values* [position]
                 |  +--rw value?      union
                 |  +--rw position    uint16
                 +--rw mo                     schc-id:matching-operator-type
                 +--rw mo-value* [position]
                 |  +--rw value?      union
                 |  +--rw position    uint16
                 +--rw cda                    schc-id:comp-decomp-action-type
                 +--rw cda-value* [position]
                    +--rw value?      union
                    +--rw position    uint16

~~~~~ 
{: #Fig-model-overview title='Overview of SCHC data model}

# IANA Considerations

This document has no request to IANA.

# Security considerations {#SecConsiderations}

This document does not have any more Security consideration than the ones already raised on {{I-D.ietf-lpwan-ipv6-static-context-hc}}

# Acknowledgements

The authors would like to thank Dominique Barthel, Carsten Bormann, Alexander Pelov. 

# YANG Module

Currently the data model is split into two parts. The first one is dedicated to SCHC identifiers and the
second one contains the rules definition. The goal is to allow some stabilities in the rule identifiers
if new SCHC identfiers are added. When the model will be stable, these two files will be merged.

~~~~
<code begins> file schc-id@2020-01-07.yang
{::include schc-id@2020-02-28.yang}
<code ends>
~~~~
{: #Fig-schc-id title="First part of the data model}

~~~~
<code begins> file schc@2020-01-23.yang
{::include schc@2020-02-28.yang}
<code ends>
~~~~
{: #Fig-schc title="Second part of the data model}


--- back
