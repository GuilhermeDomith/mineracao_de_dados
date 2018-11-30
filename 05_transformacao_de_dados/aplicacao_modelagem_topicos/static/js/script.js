$('#buscar_btn').on('click', (e) => {
    $.ajax({
        method: "GET",
        url: location.href,
        data: dados_busca()
    });
});

function dados_busca(){
    let busca = $('#busca_noticia').html();
    return JSON.stringify({'busca': busca});
}
