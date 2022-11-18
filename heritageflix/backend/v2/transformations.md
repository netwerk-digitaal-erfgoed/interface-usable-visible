# Heritageflix v2: data transformations

To convert the source data to the [target model](../../frontend/v2/datamodel.md) of the prototype.

### Dataset: RCE Beeldbank

Endpoint: https://www.collectienederland.nl/api/oai-pmh/?verb=ListRecords&metadataPrefix=edm-strict&set=rce-beeldbank

#### Heritage object

|Property in target model|Property in source model (XPath-like notation)|Remarks|
|-|-|-|
|ID|`/rdf:RDF/edm:ProvidedCHO/@rdf:about`|-|
|`rdf:type`|Fixed value: `schema:CreativeWork`|-|
|`schema:additionalType`|-|Ignore; the dataset does not contain types|
|`schema:name`|-|Ignore; the dataset does not contain names or titles|
|`schema:description`|`/rdf:RDF/edm:ProvidedCHO/dc:description`|-|
|`schema:about`|IRIs of the literals in `/rdf:RDF/edm:ProvidedCHO/dc:subject`|Requires reconciliation, from literals to IRIs. The IRIs come from terminology source CHT|
|`schema:temporal`|`/rdf:RDF/edm:ProvidedCHO/dcterms:created`; otherwise `/rdf:RDF/edm:ProvidedCHO/dc:date`|-|
|`schema:dateCreated`|Extracted year (if any) from `/rdf:RDF/edm:ProvidedCHO/dcterms:created` or `/rdf:RDF/edm:ProvidedCHO/dc:date`|-|
|`schema:contentLocation`|IRIs of the literals in `/rdf:RDF/edm:ProvidedCHO/dcterms:spatial`|Requires reconciliation, from literals to IRIs. The IRIs come from terminology source GeoNames|
|`schema:mainEntityOfPage`|`/rdf:RDF/ore:Aggregation/edm:isShownAt`|-|
|`schema:temporalCoverage`|-|Ignore; the dataset does not contain temporal coverage information|
|`schema:image`|See entity 'Media object'|-|
|`schema:creator`|See entity 'Person'|-|
|`schema:publisher`|Fixed value: `https://www.cultureelerfgoed.nl`|-|
|`schema:isBasedOn`|`/rdf:RDF/edm:ProvidedCHO/@rdf:about`|-|

#### Media object

|Property in target model|Property in source model (XPath-like notation)|Remarks|
|-|-|-|
|ID|-|Generate blank node|
|`rdf:type`|Fixed value: `schema:ImageObject`|-|
|`schema:contentUrl`|`/rdf:RDF/ore:Aggregation/edm:isShownBy/@rdf:resource`|-|
|`schema:encodingFormat`|-|Ignore; the dataset does not contain encoding formats|
|`schema:license`|`/rdf:RDF/ore:Aggregation/edm:rights/@rdf:resource`|-|

#### Person

|Property in target model|Property in source model (XPath-like notation)|Remarks|
|-|-|-|
|ID|-|Generate blank node|
|`rdf:type`|Fixed value: `schema:Person`|-|
|`schema:name`|`/rdf:RDF/edm:ProvidedCHO/dc:creator`|-|
