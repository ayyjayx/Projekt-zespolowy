const colorChange = document.createElement('style');
document.head.append(colorChange);

export function updateColor(whiteSquare, blackSquare) {
    colorChange.textContent +=`
    chess-board::part(white){
        background-color: ${whiteSquare};
    }
    chess-board::part(black){
        background-color: ${blackSquare};
    }
`;
}