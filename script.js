// Exemplo de código JavaScript para adicionar um evento de clique em um botão

document.addEventListener('DOMContentLoaded', function() {
    var myButton = document.getElementById('myButton');
    
    myButton.addEventListener('click', function() {
      alert('O botão foi clicado!');
    });
  })
  
  ;$(document).ready(function() {
    $('.slider').slick({
      autoplay: true, // habilita a reprodução automática
      autoplaySpeed: 3000, // define o tempo de exibição de cada slide (em milissegundos)
      dots: false, // desabilita os pontos de navegação
      arrows: false, // desabilita as setas de navegação
      adaptiveHeight: true
    });
  });
  