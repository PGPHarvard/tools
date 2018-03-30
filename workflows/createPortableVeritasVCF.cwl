$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: Workflow
requirements:
  - class: DockerRequirement
    dockerPull: pythonsimple 
  - class: ResourceRequirement
    coresMin: 2 
    coresMax: 10000
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.originalVCF)

inputs:
  reference: File
  refdirectory: Directory

outputs:
  out1:
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: step2/out1

steps:
  step1:
    run: tools/getFiles.cwl
    in: 
      refdirectory: refdirectory
    out: [out1]

  step2:
    scatter: originalVCF 
    scatterMethod: dotproduct
    in: 
         originalVCF: step1/out1
         reference: reference
    run: tools/createPortableVeritasVCF-tool.cwl
    out: [out1]
