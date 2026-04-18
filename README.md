# generator

**Human-Pattern Wordlist Generator**

Gerador de wordlists baseado em padrões humanos. Em vez de listas genéricas, produz combinações orientadas ao alvo: nome, apelido, datas, empresa, times, animais de estimação — os dados que as pessoas realmente usam em senhas.

---

## Funcionalidades

- Permutações de palavras-chave com variações de capitalização (`joao`, `Joao`, `JOAO`, `joAo`…)
- Substituições leet (`@`, `3`, `1`, `0`, `$`, `7`…)
- Sufixos e prefixos comuns (`!`, `@`, `123`, `#`, `007`…)
- Combinação de pares de palavras entre si (`joaoempresa`, `empresa_joao`…)
- Geração de anos (1940 até o ano atual) e combinações com palavras
- Geração de PINs e datas numéricas (modo numérico isolado)
- Filtro por comprimento mínimo e máximo
- Saída ordenada em `.txt`

---

## Uso

```bash
python3 gen.py
```

O script é totalmente interativo — só responder as perguntas. Pressione `ENTER` para pular qualquer campo.

---

## Exemplo de sessão

```
? Palavras-chave: joao, flamengo, 1985
? Incluir anos (1940 até hoje)? [s/N]: s
? Aplicar substituições leet? [s/N]: s
? Adicionar símbolos e sufixos? [s/N]: s
? Combinar pares de palavras? [s/N]: s
? Comprimento mínimo: 6
? Comprimento máximo: 20
? Nome do arquivo de saída: target_wordlist
```

Saída:

```
[✓] Wordlist gerada com sucesso!
Arquivo  : target_wordlist.txt
Entradas : 18,432
Tamanho  : 214.7 KB
```

---

## Requisitos

- Python 3.8+

---

## Aviso Legal

Use apenas em atividades autorizadas — pentest, bug bounty, recuperação de credenciais próprias. O uso contra sistemas sem permissão é ilegal.
