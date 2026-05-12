# Tasks-BE: <!-- feature-name -->

> **Module**: <!-- module --> | **DbContext**: <!-- context --> | **Total**: <!-- N --> tasks

## L0: Database (DDL + Seed)
- [ ] **T0.1: <!-- title -->** → `<!-- file_path -->` [NEW]
  <!-- 1-line: what + key constraints + schema + refs -->
- [ ] **T0.2: Permission Seed** → `scripts/seed_<!-- feature -->_permission.sql` [NEW]
  INSERT BO_FUNCTION (menu DISPLAY=1 + actions DISPLAY=0) + BO_ROLE_FUNC (Role=1). Ref: 10-permission-seed-gen.md

## L1: Entity
- [ ] **T1.1: <!-- title -->** → `<!-- file_path -->` [NEW]
  <!-- :BaseClass | ns | table | Props: list | DbSet status | Pattern ref -->

## L2: DTOs
- [ ] **T2.1: <!-- title -->** → `<!-- file_path -->` [NEW]
  <!-- :BaseClass | Props: list | Pattern ref -->

## L3: Mapper
- [ ] **T3.1: <!-- title -->** → `<!-- file_path -->` [NEW]
  <!-- Static extension methods list. !AutoMapper -->

## L4: Service
- [ ] **T4.1: Interface** → `<!-- file_path -->` [NEW]
  <!-- :IScoped | Methods list -->
- [ ] **T4.2: Implementation** → `<!-- file_path -->` [NEW]
  <!-- DI list | Business logic summary per method -->

## L5: Constants
- [ ] **T5.1: FunctionConst** → `<!-- file_path -->` [NEW]
  <!-- partial class | const=value list -->

## L6: Controller
- [ ] **T6.1: <!-- title -->** → `<!-- file_path -->` [NEW]
  <!-- :BaseController | route | attrs | endpoints with auth -->

## Traceability
<!-- Table: Design|Task|Spec mapping -->
