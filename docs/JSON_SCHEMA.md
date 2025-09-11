# JSON — Estrutura planejada

Exemplo de arquivo salvo (`.json`):

```json
{
  "meta": {
    "app": "ygra",
    "version": "0.1.0",
    "created_at": "2025-09-11T00:00:00Z"
  },
  "tree": {
    "root": {
      "id": "root",
      "label": "Raiz",
      "note": "Nó inicial",
      "children": [
        {
          "id": "n1",
          "label": "Filho A",
          "note": "",
          "children": []
        },
        {
          "id": "n2",
          "label": "Filho B",
          "note": "exemplo",
          "children": [
            { "id": "n3", "label": "Neto B1", "note": "", "children": [] }
          ]
        }
      ]
    }
  }
}
```

Regras:
- `id`: string única por nó (ex.: uuid curto).
- `label`: nome exibido.
- `note`: opcional.
- `children`: lista de nós (recursivo).
