import streamlit as st
from services import listar_produtos, cadastrar_produto, atualizar_produto, remover_produto, baixar_estoque, buscar_produto_por_id
from database import init_db

init_db()

st.title("📦 Controle de Estoque")

menu = ["📋 Lista", "➕ Novo Produto", "✏️ Editar Produto", "📉 Baixa de Estoque"]
escolha = st.sidebar.radio("Menu", menu)

if escolha == "➕ Novo Produto":
    st.subheader("Adicionar Produto")
    nome = st.text_input("Nome")
    preco = st.number_input("Preço", min_value=0.0)
    qtd = st.number_input("Quantidade", min_value=0)
    minimo = st.number_input("Estoque mínimo", min_value=0)
    categoria = st.text_input("Categoria")
    descricao = st.text_area("Descrição")

    if st.button("Salvar"):
        cadastrar_produto({
            "nome": nome,
            "preco": preco,
            "quantidade": qtd,
            "estoqueMinimo": minimo,
            "categoria": categoria,
            "descricao": descricao,
        })
        st.success("✅ Produto cadastrado com sucesso!")

elif escolha == "📋 Lista":
    st.subheader("Lista de Produtos")
    produtos = listar_produtos()
    for p in produtos:
        alerta = "🔴" if p.quantidade < p.estoqueMinimo else "🟢"
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.markdown(f"{alerta} **{p.nome}** - {p.quantidade} unidades")
        with col2:
            if st.button("✏️ Editar", key=f"edit_{p.id}"):
                st.session_state["produto_editar"] = p.id
                st.experimental_rerun()
        with col3:
            if st.button("🗑️ Excluir", key=f"del_{p.id}"):
                remover_produto(p.id)
                st.success("Produto excluído.")
                st.experimental_rerun()

elif escolha == "✏️ Editar Produto":
    st.subheader("Editar Produto")
    produto_id = st.session_state.get("produto_editar")
    if produto_id:
        produto = buscar_produto_por_id(produto_id)
        if produto:
            nome = st.text_input("Nome", produto.nome)
            preco = st.number_input("Preço", value=produto.preco)
            qtd = st.number_input("Quantidade", value=produto.quantidade)
            minimo = st.number_input("Estoque mínimo", value=produto.estoqueMinimo)
            categoria = st.text_input("Categoria", produto.categoria)
            descricao = st.text_area("Descrição", produto.descricao)

            if st.button("Salvar alterações"):
                atualizar_produto(produto_id, {
                    "nome": nome,
                    "preco": preco,
                    "quantidade": qtd,
                    "estoqueMinimo": minimo,
                    "categoria": categoria,
                    "descricao": descricao,
                })
                st.success("Produto atualizado com sucesso!")
                st.session_state.pop("produto_editar")
                st.experimental_rerun()
        else:
            st.error("Produto não encontrado.")
    else:
        st.info("Volte à lista de produtos e clique em 'Editar'.")

elif escolha == "📉 Baixa de Estoque":
    st.subheader("Baixa de Estoque (Venda)")
    produtos = listar_produtos()
    nomes = [f"{p.nome} (ID: {p.id})" for p in produtos]
    selected = st.selectbox("Selecione o produto", nomes)
    produto_id = int(selected.split("ID: ")[-1].replace(")", ""))
    quantidade = st.number_input("Quantidade vendida", min_value=1)

    if st.button("Registrar venda"):
        success = baixar_estoque(produto_id, quantidade)
        if success:
            st.success("✅ Estoque atualizado com sucesso!")
        else:
            st.error("❌ Estoque insuficiente ou produto inválido.")
