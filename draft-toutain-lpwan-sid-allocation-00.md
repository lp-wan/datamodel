---
stand_alone: true
ipr: trust200902
docname: draft-toutain-lpwan-sid-allocation-00
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

normative:
  RFC8824:
  RFC8341:
  I-D.ietf-lpwan-schc-yang-data-model:
  I-D.ietf-core-sid:
  I-D.toutain-lpwan-access-control:
  I-D.ietf-lpwan-schc-compound-ack:
informative:
  
    
--- abstract

blabla

--- middle

# Introduction

RFC9363 defines a YANG Data Model for SCHC rules. {{I-D.ietf-core-sid}} specifies the process for SID allocation and management. This document discuss of the SID allocation for RFC9363.

# SCHC YANG Data Model

The version @2023-01-18 of the SCHC YANG Data Model published in RFC 9363 contains 136 SIDs (92 for identities, 2 for features and 42 for data). {{I-D.ietf-core-sid}} indicates that the SID range for YANG Data Model specified in RFC is between 1000 and 59 000 and the maximum request pool SHOULD NOT exceed 1000. The draft also gives some pre allocated values. 

Since SIDs will be used either to represent unique identity contained
in data model and also leafs (data) forming this data model, it could
be wise to distinguish between identifiers and data.  
   
Data structures are delta encoded and included as a CBOR element, 
the size depends of the value. Deltas between -24 and +23 are coded 
on a single byte. Deltas between -256 and +255 uses 2 bytes and larger 
values corresponding to the RFC SID range will be coded into 3 bytes. 
To optimize the CORECONF representation delta should be smaller as possible
for the more frequent leafs. 

On the other hand identities are included in the CORECONF
representation and for the RFC SID range the size is constant and equal 
to 3 bytes. 

## Example
~~~~~
{5095: {1: [{4: 
        [{1: 5015,
          5: 5018,
          6: 5068,
          7: 4,
          8: 1,
          9: 5083,
          13: [{1: 0, 2: b'\x06'}]},
         {1: 5015,
          5: 5018,
          6: 2000003,
          7: 8,
          8: 1,
          9: 5083,
          13: [{1: 0, 2: b'\x00'}]},
...

{'ietf-schc:schc': {'rule': [{'entry': 
             [{'comp-decomp-action': 'ietf-schc:cda-not-sent',
               'direction-indicator': 'ietf-schc:di-bidirectional',
               'field-id': 'ietf-schc:fid-ipv6-version',
               'field-length': 4,
               'field-position': 1,
               'matching-operator': 'ietf-schc:mo-equal',
               'target-value': [{'index': 0, 'value': 'Bg=='}]},
              {'comp-decomp-action': 'ietf-schc:cda-not-sent',
               'direction-indicator': 'ietf-schc:di-bidirectional',
               'field-id': 'ietf-schc-oam:fid-icmpv6-type',
               'field-length': 8,
               'field-position': 1,
               'matching-operator': 'ietf-schc:mo-equal',
               'target-value': [{'index': 0,
               'value': 'gA=='}]},
...  
~~~~~
{: #Fig-sid title="CORECONF vs RESCONF}

The example {{Fig-sid}} gives the CORECONF structure as store in Python and its equivalent is ASCII with JSON.
The default SID numbering was used, starting from 5000 for SCHC Data Model defined in RFC9363 and 2000000 fr an experimental module for OAM. 

We can see the delta encoding. The first SID 5095 represent "ietf-schc:schc". "/ietf-schc:schc/rule" which is coded with a +1 since SID 5096 as been assigned. "/ietf-schc:schc/rule/entry" is coded with a delta of 4. Then 
a list of Field Description follows. +1 represents the leaf "ietf-schc:schc/rule/entry/comp-decomp-action" and the
value assigned to that keys contains the SID of "ietf-schc:cda-not-sent" identity.

Note that the second element contains a "field-id" belonging to the "ietf-schc-oam" module and the associate SID is 2000003.

# Recommendation for SID values 

The SCHC YANG Data Model defined in RFC 9363 will be probably be augmented, to include for instance access control
data. To keep a compact representation, delta values must be kept as small. The LPWAN working group should not use the automatic SID numbering and provide a more optimal allocation scheme for augmentation of the SCHC YANG DM. 

A first recommendation is to avoid to merge data and identity to limit the delta encoding. The distance between this two sections can be 255 SID to allow deltas on 2 bytes.

The second recommendation is to leave some unused SID around SCHC rules to allow augmentation. 




# SID for data

We propose to use a range of 100 values for the YANG DM defined in RFC9263. The next range could be used for instance by the access control Data Model which extend RFC9363.

It is also worth noting that in the current SID allocation based on alphabetical order places rule-id-value and rule-id-length, rule-nature from the 33 to 35 position. CBOR encoding will be on two bytes for each of the values. Since these three values are present in all the rules, a smaller value will optimize the CORECONF representation.

# SID allocation

We propose the following allocation scheme for RFC9363:

~~~~~
5000	- 5022 : RESERVED FOR /ietf-schc:schc 

5023	module ietf-schc
5024	data /ietf-schc:schc

5025	- 5046 : RESERVED FOR /ietf-schc:schc AND /ietf-schc:schc/rule

5047	data /ietf-schc:schc/rule
5048	data /ietf-schc:schc/rule/rule-id-length
5049	data /ietf-schc:schc/rule/rule-id-value
5050	data /ietf-schc:schc/rule/rule-nature

5051	- 5069 : RESERVED FOR /ietf-schc:schc/rule AND /ietf-schc:schc/rule/entry

5070	data /ietf-schc:schc/rule/entry
5071	data /ietf-schc:schc/rule/entry/comp-decomp-action
5072	data /ietf-schc:schc/rule/entry/comp-decomp-action-value
5073	data /ietf-schc:schc/rule/entry/comp-decomp-action-value/index
5074	data /ietf-schc:schc/rule/entry/comp-decomp-action-value/value
5075	data /ietf-schc:schc/rule/entry/direction-indicator
5076	data /ietf-schc:schc/rule/entry/field-id
5077	data /ietf-schc:schc/rule/entry/field-length
5078	data /ietf-schc:schc/rule/entry/field-position
5079	data /ietf-schc:schc/rule/entry/matching-operator
5080	data /ietf-schc:schc/rule/entry/matching-operator-value
5081	data /ietf-schc:schc/rule/entry/matching-operator-value/index
5082	data /ietf-schc:schc/rule/entry/matching-operator-value/value
5083	data /ietf-schc:schc/rule/entry/target-value
5084	data /ietf-schc:schc/rule/entry/target-value/index
5085	data /ietf-schc:schc/rule/entry/target-value/value

5086	- 5094 : RESERVED

5094	data /ietf-schc:schc/rule/ack-behavior
5095	data /ietf-schc:schc/rule/direction
5096	data /ietf-schc:schc/rule/dtag-size
5097	data /ietf-schc:schc/rule/fcn-size
5098	data /ietf-schc:schc/rule/fragmentation-mode
5099	data /ietf-schc:schc/rule/inactivity-timer
5100	data /ietf-schc:schc/rule/inactivity-timer/ticks-duration
5101	data /ietf-schc:schc/rule/inactivity-timer/ticks-numbers
5102	data /ietf-schc:schc/rule/l2-word-size
5103	data /ietf-schc:schc/rule/max-ack-requests
5104	data /ietf-schc:schc/rule/max-interleaved-frames
5105	data /ietf-schc:schc/rule/maximum-packet-size
5106	data /ietf-schc:schc/rule/rcs-algorithm
5107	data /ietf-schc:schc/rule/retransmission-timer
5108	data /ietf-schc:schc/rule/retransmission-timer/ticks-duration
5109	data /ietf-schc:schc/rule/retransmission-timer/ticks-numbers

5110	- 5115 : RESERVED FOR TIMER 

5116	data /ietf-schc:schc/rule/tile-in-all-1
5117	data /ietf-schc:schc/rule/tile-size
5118	data /ietf-schc:schc/rule/w-size
5119	data /ietf-schc:schc/rule/window-size

5120	- 5299 : RESERVED FOR 2 BYTES DELTAS

5300	identity ack-behavior-after-all-0
5301	identity ack-behavior-after-all-1
5302	identity ack-behavior-base-type
5303	identity ack-behavior-by-layer2
5304	identity all-1-data-base-type
5305	identity all-1-data-no
5306	identity all-1-data-sender-choice
5307	identity all-1-data-yes
5308	identity cda-appiid
5309	identity cda-base-type
5310	identity cda-compute
5311	identity cda-deviid
5312	identity cda-lsb
5313	identity cda-mapping-sent
5314	identity cda-not-sent
5315	identity cda-value-sent
5316	identity di-base-type
5317	identity di-bidirectional
5318	identity di-down
5319	identity di-up
5320	identity fid-base-type
5321	identity fid-coap-base-type
5322	identity fid-coap-code
5323	identity fid-coap-code-class
5324	identity fid-coap-code-detail
5325	identity fid-coap-mid
5326	identity fid-coap-option
5327	identity fid-coap-option-accept
5328	identity fid-coap-option-block1
5329	identity fid-coap-option-block2
5330	identity fid-coap-option-content-format
5331	identity fid-coap-option-etag
5332	identity fid-coap-option-if-match
5333	identity fid-coap-option-if-none-match
5334	identity fid-coap-option-location-path
5335	identity fid-coap-option-location-query
5336	identity fid-coap-option-max-age
5337	identity fid-coap-option-no-response
5338	identity fid-coap-option-observe
5339	identity fid-coap-option-oscore-flags
5340	identity fid-coap-option-oscore-kid
5341	identity fid-coap-option-oscore-kidctx
5342	identity fid-coap-option-oscore-piv
5343	identity fid-coap-option-proxy-scheme
5344	identity fid-coap-option-proxy-uri
5345	identity fid-coap-option-size1
5346	identity fid-coap-option-size2
5347	identity fid-coap-option-uri-host
5348	identity fid-coap-option-uri-path
5349	identity fid-coap-option-uri-port
5350	identity fid-coap-option-uri-query
5351	identity fid-coap-tkl
5352	identity fid-coap-token
5353	identity fid-coap-type
5354	identity fid-coap-version
5355	identity fid-ipv6-appiid
5356	identity fid-ipv6-appprefix
5357	identity fid-ipv6-base-type
5358	identity fid-ipv6-deviid
5359	identity fid-ipv6-devprefix
5360	identity fid-ipv6-flowlabel
5361	identity fid-ipv6-hoplimit
5362	identity fid-ipv6-nextheader
5363	identity fid-ipv6-payload-length
5364	identity fid-ipv6-trafficclass
5365	identity fid-ipv6-trafficclass-ds
5366	identity fid-ipv6-trafficclass-ecn
5367	identity fid-ipv6-version
5368	identity fid-oscore-base-type
5369	identity fid-udp-app-port
5370	identity fid-udp-base-type
5371	identity fid-udp-checksum
5372	identity fid-udp-dev-port
5373	identity fid-udp-length
5374	identity fl-base-type
5375	identity fl-token-length
5376	identity fl-variable
5377	identity fragmentation-mode-ack-always
5378	identity fragmentation-mode-ack-on-error
5379	identity fragmentation-mode-base-type
5380	identity fragmentation-mode-no-ack
5381	identity mo-base-type
5382	identity mo-equal
5383	identity mo-ignore
5384	identity mo-match-mapping
5385	identity mo-msb
5386	identity nature-base-type
5387	identity nature-compression
5388	identity nature-fragmentation
5389	identity nature-no-compression
5390	identity rcs-algorithm-base-type
5391	identity rcs-crc32
5392	feature compression
5393	feature fragmentation

5394	- 5500 : RESERVED FOR IDENTITY
~~~~ 

For instance {{I-D.toutain-lpwan-access-control}} augments the model with "ac-modify-set-of-rules" at the top level, "ac-modify-compression-rule" for each compression rule, "ac-modify-field" in each Field Description of a compression rule and finally "ac-modify-timers" in fragmentation rules. Delta representation will be on 1 byte.

The following SIDs could be assigned:

* 5022: ac-modify-set-of-rules
* 5051: ac-modify-compression-rule
* 5069: ac-modify-field
* 5068: ac-modify-timers

{{I-D.ietf-lpwan-schc-compound-ack}} augments the model for fragmentation, with 3 identity and two leaves. 
identities can get a SID 5394 to 5396 and the two SIDs for the leaves can be 5120 and 5122. There delta representations will be coded on 2 bytes. 


--- back



# Security Considerations

TBD

# IANA Considerations

TBD