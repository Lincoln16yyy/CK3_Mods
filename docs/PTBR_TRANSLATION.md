# Jogo em português (PT-BR)

O CK3 1.20.1 não tem idioma português: `game/localization/languages.yml` lista nove
idiomas (inglês, francês, alemão, polonês, espanhol, chinês simplificado, russo, coreano,
japonês). Nenhum mod cria um idioma novo — a única forma de jogar em PT-BR é **substituir
o pacote de um idioma que já existe**.

## Fonte usada

Tradução comunitária **"Tradução PT-BR"**, de Emerson Antunes
(Steam Workshop `3728653302`, Paradox Mods `144303`, repositório
`antunesemerson/mod-ck3-traducao-pt-br`, último commit 2026-07-10).

Ela foi feita para substituir o pacote **espanhol** (`localization/spanish/*_l_spanish.yml`),
o que obrigaria a jogar com o jogo em "Español". Como o seu jogo está em inglês, o pacote
foi convertido por `tools/build_ptbr_pack.py` para substituir o **inglês**.

## O que o script faz

1. Lê o vanilla inglês instalado (fonte de verdade de quais chaves existem em 1.20.1).
2. Lê o pacote comunitário em `localization/spanish/`.
3. Grava `localization/replace/english/<mesmo caminho>_l_english.yml` com:
   - cabeçalho `l_english:`;
   - todas as linhas traduzidas, sem alteração;
   - **toda chave que a tradução não tem, copiada do inglês** — assim nenhuma chave
     aparece crua na tela.
4. Imprime o relatório de cobertura.

```bash
python3 tools/build_ptbr_pack.py \
  --source /caminho/mod-ck3-traducao-pt-br/traducao_pt_br \
  --game  "$HOME/Downloads/Crusader Kings III/Crusader Kings III/game" \
  --out   "$HOME/.config/hydralauncher/wine-prefixes/1158310/drive_c/users/steamuser/Documents/Paradox Interactive/Crusader Kings III/mod/traducao_ptbr_120"
```

## Cobertura medida (vanilla 1.20.1)

| Métrica | Valor |
| --- | --- |
| Arquivos de localização gerados | 1172 |
| Chaves traduzidas para PT-BR | 286.967 |
| Chaves com fallback em inglês (lacunas da tradução) | 8.063, em 268 arquivos |
| Chaves vanilla cobertas dentro dos arquivos substituídos | 295.030 de 307.119 (**96,1%**) |
| Chave crua restante nos arquivos substituídos | **0** |
| Arquivos vanilla sem tradução (seguem em inglês) | 78 (≈3,9% das chaves) |
| Arquivos do pacote ignorados (chaves que não existem em 1.20.1) | 16 |

Os 78 arquivos sem tradução são conteúdo mais novo (vários de DLC `pam`), posterior à
versão que a tradução cobre. Eles continuam carregando do vanilla, em inglês — não quebram
nada, apenas aparecem em inglês.

## Instalação

O pacote já foi gerado em
`.../Crusader Kings III/mod/traducao_ptbr_120` com `descriptor.mod` e
`traducao_ptbr_120.mod` (`supported_version="1.20.*"`). No launcher:

1. Ative **Traducao PT-BR (compat 1.20.1)**.
2. Mantenha o jogo em **English** (o pacote substitui o inglês; não troque para espanhol).
3. Deixe-o **abaixo** dos mods de conteúdo, para que textos de mods que também traduzem
   o inglês (como o Smart Realm Director) não sejam sobrescritos por engano.

## Limitações e cuidados

- **Não é trabalho meu**: a tradução é de Emerson Antunes. O repositório guarda apenas o
  script que a converte; os 29 MB de texto traduzido ficam fora do git, por direitos e
  por tamanho. Mantenha os créditos se redistribuir.
- **Nada foi verificado em jogo.** A checagem é estática: BOM, cabeçalho, e o conjunto de
  chaves de cada arquivo gerado contendo todas as chaves vanilla correspondentes.
- `localization/replace/` é a pasta documentada pela Paradox para sobrescrever textos
  existentes; ordem de carregamento ainda precisa ser confirmada na prática.
- Se você atualizar a tradução comunitária, rode o script de novo — é idempotente.
- Chaves de mods que não sejam o SRD continuam como cada mod definir.

## Próximos passos possíveis

1. Traduzir os 78 arquivos restantes (mesma estrutura, chaves já mapeadas pelo script).
2. Revisar termos de jogo (títulos, governo, obrigações) para consistência com o uso
   brasileiro da comunidade.
3. Comparar com a versão do Nexus (`Traducao PTBR`, v1.20.1.2), que é mais recente que a
   do GitHub, caso o download manual seja possível.
