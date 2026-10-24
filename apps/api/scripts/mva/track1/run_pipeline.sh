#!/usr/bin/env bash
# Genome-wide variant prioritisation for Track 1, end to end.
#
#   HF_TOKEN=... ./run_pipeline.sh <workdir> "<comma-separated proband HPO ids>"
#
# Reaches the causal gene from the callset plus the phenotype. NO STAGE NAMES A GENE.
# The proband's HPO terms are supplied on the command line and never committed, because
# the challenge data is gated and must not be redistributed.
set -euo pipefail
WORK="${1:?usage: run_pipeline.sh <workdir> \"<HPO ids>\"}"
TERMS="${2:?supply the proband HPO terms, comma-separated}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${HF_TOKEN:?the challenge dataset is gated; export HF_TOKEN}"
mkdir -p "$WORK"; cd "$WORK"

REPO=SageBio/mva-hackathon-2026-data
BASE="https://huggingface.co/datasets/$REPO/resolve/main"
VCF=WGS_EX2312012_HGWCNDSX7.vcf.gz

echo "== 0. reference data (public) =="
[ -f gff3.gz ]  || curl -sL -o gff3.gz "https://ftp.ensembl.org/pub/current_gff3/homo_sapiens/$(
  curl -s https://ftp.ensembl.org/pub/current_gff3/homo_sapiens/ \
  | grep -oE 'Homo_sapiens\.GRCh38\.[0-9]+\.gff3\.gz' | sort -u | head -1)"
[ -f hp.obo ]   || curl -sL -o hp.obo  "https://purl.obolibrary.org/obo/hp.obo"
[ -f g2p.txt ]  || curl -sL -o g2p.txt "https://purl.obolibrary.org/obo/hp/hpoa/genes_to_phenotype.txt"

echo "== 0b. the gated callset (streamed, delete when done) =="
for f in "$VCF" "$VCF.tbi"; do
  [ -f "$f" ] || curl -sL --fail -H "Authorization: Bearer $HF_TOKEN" -o "$f" "$BASE/$f"
done

echo "== 1. CDS index over every protein-coding gene =="
[ -f cds_index.json.gz ] || python3 "$HERE/build_cds_index.py" --gff3 gff3.gz --out cds_index.json.gz

echo "== 2. coding + biallelic-compatible =="
python3 "$HERE/stage12_candidates.py" --vcf "$VCF" --index cds_index.json.gz --out stage2.json

echo "== 3. VEP: impact and gnomAD rarity, then re-test biallelic =="
python3 "$HERE/stage3_annotate.py" --in stage2.json --out stage3.json --cache vep_cache.json

echo "== 4. rank by phenotype similarity =="
python3 "$HERE/stage5_phenotype_rank.py" --in stage3.json --obo hp.obo --g2p g2p.txt \
  --terms "$TERMS" --top 25

cat <<'EOT'

Reminder: the hackathon DTA requires the callset to be deleted from every environment.
    rm -f WGS_EX2312012_HGWCNDSX7.vcf.gz*
EOT
