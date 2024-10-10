<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cryptage Caesar Cipher</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Cryptage avec Caesar Cipher</h1>
    <form method="POST">
        <label for="text">Texte à chiffrer :</label><br>
        <input type="text" id="text" name="text" required><br><br>
        
        <label for="shift">Décalage :</label><br>
        <input type="number" id="shift" name="shift" required><br><br>
        
        <button type="submit">Chiffrer</button>
    </form>

    <?php
    error_reporting(E_ALL);
    ini_set('display_errors', 1);

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Échapper les entrées utilisateur pour éviter les attaques XSS
        $text = htmlspecialchars($_POST["text"]);
        $shift = (int)$_POST["shift"];

        // Fonction pour le cryptage Caesar Cipher
        function caesarCipher($text, $shift) {
            $result = "";
            $shift = $shift % 26;

            for ($i = 0; $i < strlen($text); $i++) {
                $char = $text[$i];

                if (ctype_alpha($char)) {
                    $asciiOffset = ctype_upper($char) ? 65 : 97;
                    $result .= chr((ord($char) - $asciiOffset + $shift) % 26 + $asciiOffset);
                } else {
                    $result .= $char; // Garder les caractères non alphabétiques inchangés
                }
            }
            return $result;
        }

        $encrypted_text = caesarCipher($text, $shift);
        echo "<h2>Texte chiffré : $encrypted_text</h2>";
    }
    ?>
</body>
</html>
