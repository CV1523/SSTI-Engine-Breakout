<?php
// index.php
require_once 'vendor/autoload.php';

use Latte\Engine;
use Latte\Sandbox\SecurityPolicy;

$latte = new Engine();
// Set a dedicated compilation cache directory
$latte->setTempDirectory(__DIR__ . '/temp');

$current_mode = isset($_GET['mode']) ? $_GET['mode'] : 'standard';
$user_input = isset($_POST['input']) ? $_POST['input'] : '';
$result = null;
$error = null;

// Configure the Sandbox Policy if Sandbox mode is active
if ($current_mode === 'sandbox') {
    $policy = new SecurityPolicy();
    // In a production app, you would whitelist specific safe tags/filters here.
    // Leaving it blank creates a strict default lock down.
    
    // 1. Pass the policy object to the engine (Latte v3 style)
    $latte->setPolicy($policy);
    
    // 2. Explicitly toggle sandbox enforcement mode on
    $latte->setSandboxMode(true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($user_input)) {
    try {
        // VULNERABLE POINT: Dynamically compiling raw user input directly into a template file
        $temp_template = __DIR__ . '/temp_exploit.latte';
        file_put_contents($temp_template, $user_input);
        
        // Clear internal Latte engine memory cache to ensure our payload updates instantly
        // (Wiping the temp folder structures programmatically handles timestamp caching)
        array_map('unlink', glob(__DIR__ . '/temp/*'));

        // Render the template file cleanly
        $result = $latte->renderToString($temp_template);
    } catch (\Exception $e) {
        $error = $e->getMessage();
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>SSTI Lab - PHP Latte Engine</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: #121214; color: #e1e1e6; }
        .container { background: #202024; border-radius: 8px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #29292e; }
        input[type="text"] { width: 75%; padding: 12px; margin: 10px 0; border: 1px solid #29292e; border-radius: 4px; font-size: 14px; font-family: monospace; background: #121214; color: #fff; }
        button { padding: 12px 24px; background: #1e88e5; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: bold; }
        button:hover { background: #1565c0; }
        .result { margin-top: 20px; padding: 15px; background: #121214; color: #33ff33; border-radius: 4px; border-left: 5px solid #27ae60; font-family: 'Courier New', Courier, monospace; }
        .error { color: #ff4d4d; border-left-color: #e74c3c; background: #2d1a1a; }
        .info { background: #29292e; padding: 15px; margin-bottom: 20px; border-left: 4px solid #1e88e5; border-radius: 4px; color: #c4c4cc; }
        select { padding: 10px; margin: 10px 0; border-radius: 4px; border: 1px solid #29292e; background: #121214; color: #fff; width: 100%; max-width: 400px; }
        pre { white-space: pre-wrap; word-wrap: break-word; margin: 0; }
    </style>
</head>
<body>
    <h1>🧪 SSTI Lab - PHP Latte Engine</h1>
    
    <div class="container">
        <h3>⚙️ Engine Mode Configuration</h3>
        <form method="GET" action="">
            <label>Select operating mode:</label><br>
            <select name="mode" onchange="this.form.submit()">
                <option value="standard" <?php echo $current_mode === 'standard' ? 'selected' : ''; ?>>Standard Mode (Unrestricted)</option>
                <option value="sandbox" <?php echo $current_mode === 'sandbox' ? 'selected' : ''; ?>>Latte Sandbox Mode (Restricted Environment)</option>
            </select>
        </form>
    </div>
    
    <div class="container">
        <h3>💉 Inject Payload</h3>
        <form method="POST" action="?mode=<?php echo htmlspecialchars($current_mode); ?>">
            <input type="text" name="input" placeholder="{$control}" required value="<?php echo htmlspecialchars($user_input); ?>">
            <button type="submit">Run Template</button>
        </form>
        
        <?php if ($result !== null): ?>
        <div class="result">
            <h4>📄 Output:</h4>
            <pre><?php echo $result; ?></pre>
        </div>
        <?php endif; ?>
        
        <?php if ($error !== null): ?>
        <div class="result error">
            <h4>❌ Engine Error:</h4>
            <pre><?php echo htmlspecialchars($error); ?></pre>
        </div>
        <?php endif; ?>
    </div>
</body>
</html>