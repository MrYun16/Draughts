# introduction
this is my orogram
Example:
https://mermaid.live/

# class diagram
here is my diagram
```mermaid
classDiagram
    Player <|-- AI
    AI <|-- randomAI
    Game o-- Player
    Gui o-- Game
    Game o-- Piece
    Piece <|-- Stone
    Piece <|-- King

    class Gui{
      +String square1clr
      +String square2clr
      +String gameOnGoing
      -playWindow()
      -squareClicked()
      -updateBoard()
      -run()
    }

    class Game{
      -jumpingPiece
      -board
      -boardHistory
      -PiecesHistory
      -currentPlayerHistory
      -jumpingPieceHistory
      -prepareBoard()
      -undo()
      -ownPiece()
      -getOwnPiece()
      -play()
      -vacantSquare()
      -playerCanJump()
      -canJump()
      -isJump()
      -isMove()
      -move()
      -jump()
      -at()
      -switchTurn()
      -getWinner()
      -updateHistory()
    }
    class Player{
      -numPieces
      -name
      -direction
      -colour
      -time
      -isAI
      +amendNumPieces()
    }
    class Piece{
      -colour
      -direction
      -x
      -y
      -updateXY()
    }
    class Stone{
      -isStone
      -vectors
      -promoted()
    }
    class King{
      -isStone
      -vectors
    }
    class AI{
        -play()
    }
    class randomAI{
        pass
    }
            



