<?php
// index.php
require_once 'vendor/autoload.php';

use Illuminate\Container\Container;
use Illuminate\Events\Dispatcher;
use Illuminate\Filesystem\Filesystem;
use Illuminate\View\Compilers\BladeCompiler;
use Illuminate\View\Engines\CompilerEngine;
use Illuminate\View\Engines\EngineResolver; // Fixed Class Name
use Illuminate\View\Factory;
use Illuminate\View\FileViewFinder;

// 1. Set up the container instances
$container = Container::getInstance();
$container->instance('files', new Filesystem());
$container->instance('events', new Dispatcher($container));

// Configuration Directories
$viewPaths = [__DIR__ . '/views'];
$compiledPath = __DIR__ . '/cache';

// 2. Explicitly bind the compiler singleton
$container->singleton('blade.compiler', function () use ($compiledPath, $container) {
    return new BladeCompiler($container['files'], $compiledPath);
});

// 3. Register the engine solver correctly
$engines = new EngineResolver(); // Fixed Class instantiation
$engines->register('blade', function () use ($container) {
    return new CompilerEngine($container['blade.compiler']);
});

$finder = new FileViewFinder($container['files'], $viewPaths);
$viewFactory = new Factory($engines, $finder, $container['events']);
$viewFactory->setContainer($container);

// Lab Request Logic Execution
$user_input = isset($_POST['input']) ? $_POST['input'] : '';
$result = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($user_input)) {
    try {
        // VULNERABLE AXIS: Dynamic overwrite forcing on-the-fly execution structure
        $temp_view_path = __DIR__ . '/views/exploit.blade.php';
        file_put_contents($temp_view_path, $user_input);
        
        // Render via Factory engine instance
        $result = $viewFactory->make('exploit')->render();
    } catch (\Exception $e) {
        $error = $e->getMessage();
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>SSTI Lab - PHP Blade Engine</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: #121214; color: #e1e1e6; }
        .container { background: #202024; border-radius: 8px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #29292e; }
        input[type="text"] { width: 75%; padding: 12px; margin: 10px 0; border: 1px solid #29292e; border-radius: 4px; font-size: 14px; font-family: monospace; background: #121214; color: #fff; }
        button { padding: 12px 24px; background: #ff2d20; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: bold; }
        button:hover { background: #b31e15; }
        .result { margin-top: 20px; padding: 15px; background: #121214; color: #33ff33; border-radius: 4px; border-left: 5px solid #27ae60; font-family: 'Courier New', Courier, monospace; }
        .error { color: #ff4d4d; border-left-color: #e74c3c; background: #2d1a1a; }
        .info { background: #29292e; padding: 15px; margin-bottom: 20px; border-left: 4px solid #ff2d20; border-radius: 4px; color: #c4c4cc; }
        pre { white-space: pre-wrap; word-wrap: break-word; margin: 0; }
    </style>
</head>
<body>
    <h1>🧪 SSTI Lab - PHP Blade Engine</h1>
    
    <div class="info">
        <strong>🎯 Goal:</strong> Execute math, read internal parameters, or invoke system commands.
    </div>
    
    <div class="container">
        <h3>💉 Inject Payload</h3>
        <form method="POST" action="">
            <input type="text" name="input" placeholder="{{ 7*7 }}" required value="<?php echo htmlspecialchars($user_input); ?>">
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