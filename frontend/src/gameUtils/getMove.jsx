import React, { useEffect } from "react";

export function getMove() {
    useEffect(() => {
        React.board.addEventListener('drop', (e) => {
            const { source, target, piece, orientation } = e.detail;
            console.log('Source: ' + source)
            console.log('Target: ' + target)
            console.log('Piece: ' + piece)
            console.log('Orientation: ' + orientation)
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        });
    }, []);
}