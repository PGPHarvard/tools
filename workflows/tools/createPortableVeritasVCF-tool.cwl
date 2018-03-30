$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    coresMin: 2
    ramMin: 10000
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.originalVCF)
  - class: DockerRequirement
    dockerPull: pythonsimple
    
hints:
  arv:RuntimeConstraints:
    keep_cache: 4096

baseCommand: python 
arguments: 
  - $(inputs.script[0])
inputs:
  script:
    type: File[]
    default:
      - class: File
        location: ../scripts/make_portable_veritas_vcf.py
      - class: File
        location: ../scripts/combine_veritas_vcf.py
  originalVCF:
    type: File
    inputBinding:
      position: 1
  reference:
    type: File 
    inputBinding:
      position: 2
outputs:
  out1:
    type: File[] 
    outputBinding:
      glob: "*portable*"

