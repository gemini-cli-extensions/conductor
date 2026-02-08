# Flutter Code Style Guide

This guide extends the [Dart Code Style Guide](./dart.md) with Flutter-specific conventions and best practices for building robust, maintainable Flutter applications.

## 1. Project Structure

### 1.1. Feature-Based Directory Structure

```
lib/
├── src/
│   ├── core/
│   │   ├── constants/
│   │   ├── errors/
│   │   ├── extensions/
│   │   ├── theme/
│   │   └── utils/
│   ├── common/
│   │   ├── widgets/
│   │   └── pages/
│   └── di/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   └── datasources/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── bloc/
│   │       ├── pages/
│   │       └── widgets/
│   └── feature_b/
├── main.dart
└── app.dart
```

### 1.2. File Naming Conventions

- **Models/Entities:** `user_model.dart`, `product_entity.dart`
- **Repositories:** `user_repository.dart`
- **Data Sources:** `user_remote_datasource.dart`, `user_local_datasource.dart`
- **Use Cases:** `login_usecase.dart`, `get_products_usecase.dart`
- **Blocs/Cubits:** `auth_bloc.dart`, `user_cubit.dart`
- **Pages/Screens:** `login_page.dart`, `home_screen.dart`
- **Widgets:** `user_card.dart`, `custom_button_widget.dart`

## 2. Flutter Widgets

### 2.1. Stateless vs Stateful Widgets

- **USE** `StatelessWidget` for UI that depends only on final variables and BuildContext.
- **USE** `StatefulWidget` when you need mutable state or initialization logic.
- **PREFER** using `ConsumerStatefulWidget` with Provider/ Riverpod for state management.
- **PREFER** extracting complex UI into smaller reusable widgets.

### 2.2. Widget Construction

```dart
// BAD: Too many positional arguments
MyWidget('param1', 'param2', true, null);

// GOOD: Named parameters with defaults
MyWidget({
  required this.title,
  this.subtitle = '',
  this.isActive = false,
  this.onTap,
});
```

### 2.3. Const Constructors

- **DO** use `const` constructors for widgets that are immutable.
- **DO** wrap child widgets with `const` when possible.

```dart
// GOOD
const SizedBox(height: 16);

// GOOD - Using const in lists
Column(
  children: const [
    Text('Hello'),
    Text('World'),
  ],
);
```

## 3. State Management

### 3.1. General Principles

- **PREFER** a single source of truth per feature.
- **DO** keep business logic out of UI widgets.
- **PREFER** reactive state management (Bloc, Riverpod, GetX) over manual setState.
- **DO** dispose of controllers, cubits, and listeners in `dispose()`.

### 3.2. Bloc Pattern

```dart
// Bloc
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  final IncrementCounterUseCase useCase;
  
  CounterBloc(this.useCase) : super(CounterInitial()) {
    on<Increment>(_increment);
  }

  void _increment(Increment event, Emitter<Emitter> emit) {
    final result = useCase(event.value);
    emit(CounterLoaded(result));
  }
}

// Usage in widget
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('Count: ${state.count}');
  },
);
```

### 3.3. Riverpod

```dart
// Provider
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
}

// ConsumerWidget
class HomePage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('Count: $count');
  }
}
```

## 4. Error Handling

### 4.1. Custom Exceptions

```dart
sealed class AppException implements Exception {
  final String message;
  AppException(this.message);
}

class NetworkException extends AppException {
  NetworkException([super.message = 'Network error occurred']);
}

class ValidationException extends AppException {
  final Map<String, String> errors;
  ValidationException(this.errors) : super('Validation failed');
}
```

### 4.2. Error Boundaries

```dart
class ErrorBoundary extends StatelessWidget {
  final Widget child;
  final VoidCallback? onRetry;

  const ErrorBoundary({
    super.key,
    required this.child,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialBanner(
      // Implementation for error display and retry
    );
  }
}
```

## 5. Testing

### 5.1. Widget Testing

```dart
void main() {
  testWidgets('Counter increments', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    expect(find.text('0'), findsOneWidget);
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();
    expect(find.text('1'), findsOneWidget);
  });
}
```

### 5.2. Bloc Testing

```dart
void main() {
  late CounterBloc bloc;

  setUp(() {
    bloc = CounterBloc();
  });

  test('initial state is CounterInitial', () {
    expect(bloc.state, equals(CounterInitial()));
  });

  blocTest<CounterBloc, CounterState>(
    'emits [CounterLoaded] when Increment is added',
    build: () => bloc,
    act: (bloc) => bloc.add(Increment(1)),
    expect: () => [equals(CounterLoaded(1))],
  );
}
```

### 5.3. Repository Testing

```dart
void main() {
  late UserRepository repository;
  late MockUserDatasource datasource;

  setUp(() {
    datasource = MockUserDatasource();
    repository = UserRepository(datasource);
  });

  test('getUser returns user on success', () async {
    const user = User(id: '1', name: 'John'));
    when(datasource.getUser('1')).thenAnswer((_) async => user);

    final result = await repository.getUser('1');

    expect(result, equals(user));
  });
}
```

## 6. Performance Optimization

### 6.1. List Views

```dart
// GOOD: Use ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ListTile(
    title: Text(items[index].title),
  ),
);

// GOOD: Use addAutomaticKeepAlive to preserve scroll position
CustomScrollView(
  slivers: [
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => MyWidget(),
        childCount: 100,
      ),
    ),
  ],
);
```

### 6.2. Image Optimization

```dart
// GOOD: Use specific cache dimensions
Image.network(
  'url',
  cacheWidth: 300,
  cacheHeight: 300,
  loadingBuilder: (context, child, progress) {
    if (progress == null) return child;
    return CircularProgressIndicator();
  },
);
```

### 6.3. Const Widgets

```dart
// GOOD: Extract const widgets
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        const HeaderWidget(),
        const ContentWidget(),
      ],
    );
  }
}
```

## 7. Internationalization

### 7.1. ARB Files

```arb
{
  "@@locale": "en",
  "helloWorld": "Hello World",
  "@helloWorld": {
    "description": "Greeting message"
  },
  "greeting": "{name} says hello",
  "@greeting": {
    "description": "Personalized greeting",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  }
}
```

### 7.2. Usage

```dart
// GOOD
Text(AppLocalizations.of(context)!.helloWorld);

// GOOD: with parameters
Text(AppLocalizations.of(context)!.greeting('John'));
```

## 8. Additional Resources

- [Effective Dart](https://dart.dev/effective-dart)
- [Flutter Official Docs](https://docs.flutter.dev/)
- [Flutter Best Practices](https://medium.com/flutter-community/flutter-best-practices-and-tips-7dc8552d01f4)
- [Bloc Library](https://bloclibrary.dev/)
- [Riverpod](https://riverpod.dev/)
